import os
import jwt
import json
import datetime
from .func.code import Code
from .func.AnsibleAd import PlayRun
from .func.AnsibleCallBack import SupervisorResultCallback, CronResultCallback
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import *
from .serializers import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class CheckRequestMixin:
    def check_params(self, *args):
        for item in args:
            if item is None:
                return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class JSONReponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().renderer(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class Upload(APIView):
    def get(self, request, format=None):
#        data = list(SupervisorHost.objects.all().values())
        return Response(data)

    def post(self, request, format=None):
        request.POST.get("")
        pass


class CodeChange(APIView):
    def post(self, request, format=None):
        ip = request.POST.get("ip")
        wxCode = request.POST.get("wxCode")
        ssh = Code(ip, wxCode, passwd="justdoit")
        ssh.connect()
        rest = ssh.sed_code() 
        return Response({"rest": rest})


class LoginAPI(APIView):
    KEY = '!@2#3$%d6?2&19(*)*#f123zfnvsdfdsfd#@!95^%$<fs1'

    def get(self, request, format=None):
        action = request.GET.get("action", None)
        if action != "get":
            return Response("FORBIDDEN", status.HTTP_403_FORBIDDEN)
        token = request.COOKIES.get("X-User-Authorization", None)
        print(request.COOKIES)
        if token is None:
            return Response({"message": "Not Login", "logined": 0})
        try:
            decoded = jwt.decode(token.encode(), self.KEY, algorithm="HS512")
            username = decoded.get("username", None)
            Login.objects.get(username=username)
            return Response({"message": "Aleardy login", "logined": 1})
        except Exception as e:
            return Response({"message": e, "logined": 0})

    def delete(self, request, format=None):
        """
        注销,清除token
        """
        action = request.GET.get("action", None)
        if action != "del":
            return Response("FORBIDDEN", status.HTTP_403_FORBIDDEN)
        try:
            response = Response({"message": "You're logout", "logined": 0, "logout": 1})
            response.delete_cookie("X-User-Authorization")
#            del request.session["X-User-Authorization"]
        except KeyError:
            pass
        return response
            
    def post(self, request, format=None):
        """
          POST: {username: XXX, password: XXX}
        """
        post_data = json.loads(request.body.decode())
        username = post_data.get("username", None)
        password = post_data.get("password", None)
        if username is None or password is None:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        try:
            Login.objects.get(username=username, password=password)
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
            payload = {"username": username, "exp": exp}
            token = jwt.encode(payload, self.KEY, algorithm="HS512").decode()
            #request.session["X-User-Authorization"] = token
            expires = datetime.datetime.now() + datetime.timedelta(days=3)
            response = Response({"login": "success"})
            response.set_cookie('X-User-Authorization', token, httponly=True, expires=expires)
            return response
        except Login.DoesNotExist:
            return Response({"login": "faile"})


class AddSupervisor(APIView):
    db = SupervisorHost

    def __update_or_create(self, host, project="", status="", display="1", is_group="0"):
        """
          根据传入的host,project字段判断是否存在，
          若存在,则执行额外参数的 update 操作
          否则，执行 create 操作
        """
        db_object = self.db.objects.filter(host=host, project=project)
        if db_object:
            db_object.update(status=status, display=display, is_group=is_group)
        else:
            db_object.create(host=host,
                             project=project,
                             status=status,
                             display=display,
                             is_group=is_group)

    def put(self, request, format=None):
        """
          POST: { scan: 0, is_group: 0}
          is_group:int, 0为获取进程信息, 1为获取组信息
        """
        post_data = json.loads(request.body.decode())
        is_group = post_data.get("is_group", None)
        if post_data.get("scan", None) != 0:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        ans_shell = "shell"
        ans_command = """/bin/bash -lc 'supervisorctl status'"""
        hosts = "all_user"
        playrun = PlayRun()
        scan_result = playrun.run([(ans_shell, ans_command)], hosts=hosts)
        host_set = set()
        for host, value in scan_result.items():
            stdout = value.get('stdout')
            if isinstance(stdout, str) and stdout.startswith(r'unix:///'):
                self.__update_or_create(host=host, project=stdout, status="未启动服务")
                continue
            for item in stdout:
                project, status = item
                host_set.add((host, project))
                self.__update_or_create(host=host, project=project, status=status)

                cut_data = project.split(":")
                if len(cut_data) == 2:
                    group_mid, _ = cut_data
                    group = group_mid + ':*'
                    host_set.add((host, group))
                    self.__update_or_create(host=host, project=group, is_group="1")
            db_set = { (db.host, db.project) for db in self.db.objects.filter(host=host) }
            diff = db_set.difference(host_set)
            for diff_item in diff:
                host, project = diff_item
                self.db.objects.filter(host=host, project=project).update(display="0")
        finally_result = list(self.db.objects.filter(is_group=is_group, display="1").values())
        return Response(finally_result)

    def post(self, request, format=None):
        post_data = json.loads(request.body.decode()) 
        host = post_data.get("host", None)
        project = post_data.get("project", None)
        name = post_data.get("name", None)
        describe = post_data.get("describe", None)
        is_group = post_data.get("is_group", None)
        self.db.objects.filter(host=host, project=project).update(name=name, describe=describe)
        finally_result = list(self.db.objects.filter(is_group=is_group, display="1").values())
        return Response(finally_result)


    def get(self, request, format=None):
        is_group = request.GET.get("is_group", None)
        if is_group is None:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        finally_result = list(self.db.objects.filter(is_group=is_group, display="1").values())
        return Response(finally_result)
        

class ControlSupervisor(APIView):
    def post(self, request, format=None):
        post_data = json.loads(request.body.decode())
        hosts = post_data.get("host", None)
        action = post_data.get("action", None)
        project = post_data.get("project", None)
        if hosts is None or action is None or project is None:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        ans_module = "shell"
        ans_command = """/bin/bash -lc 'supervisorctl {action} {project}'""".format(action=action, project=project)
        playrun = PlayRun(callback=SupervisorResultCallback)
        can_result = playrun.run([(ans_module, ans_command)], hosts=hosts)
        return Response({"rest": 0})


class CrontabAPI(APIView):
    db = CrontabHost

    def __update_or_create(self, cron_host="", cron_user="", crontab="", cron_update=None):
        if crontab.startswith(r"#"):
            cron_update = crontab.strip("#")
        else:
            cron_update = "#" + crontab 
        db_object = self.db.objects.filter(cron_host=cron_host, cron_user=cron_user, crontab=crontab)
        db_object_update = self.db.objects.filter(cron_host=cron_host, cron_user=cron_user, crontab=cron_update)
        if db_object:
            db_object.update(crontab=crontab)
        elif db_object_update:
            db_ojbect.update(crontab=crontab)
        else:
            self.db.objects.create(cron_host=cron_host, cron_user=cron_user, crontab=crontab)
            

    def put(self, request, format=None):
        ans_module = "script"
        ans_command = os.path.join(BASE_DIR, "shell/get_cron.sh")
        hosts = "all_user"
        playrun = PlayRun(callback=CronResultCallback)
        can_result = playrun.run([(ans_module, ans_command)], hosts=hosts)
        host_set = set()
        for cron_host, values in can_result.items():
            for stdout in values.get("stdout"):
                cron_user, cron_list = stdout
                for crontab in cron_list:
                    host_set.add((cron_host, cron_user, crontab))
                    self.__update_or_create(cron_host=cron_host,
                                            cron_user=cron_user,
                                            crontab = crontab)
        db_set = set((db["cron_host"],
                      db["cron_user"],
                      db["crontab"]) for db in self.db.objects.values())
        diff = db_set.difference(host_set)
        for diff_item in diff:
            cron_host, cron_user, crontab = diff_item
            self.db.objects.filter(cron_host=cron_host, cron_user=cron_user, crontab=crontab).delete()
        return Response({"rest": 0})
