import os
import json
from .func.code import Code
from .func.AnsibleAddSupervisor import PlayRun
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import *
from .serializers import *

class CheckRequestMixin:
    def check_params(self, *args):
        for item in args:
            if item is None:
                return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)


class SupervisorDBMixin:
    db = SupervisorHost

    def write_db(self, command, hosts="all_user"):
        host_set = set()
        playrun = PlayRun()
        scan_result = playrun.run([("shell", command)], hosts=hosts)
        print(scan_result)
        for host, value in scan_result.items():
            stdout = value.get('stdout') 
            if isinstance(stdout, str) and stdout.startswith(r'unix:///'):
                self.db.objects.filter(host=host).update(display="0")
                self.db.objects.create(host=host, project=stdout, status="未启动服务")
                continue
            for item in stdout:
                project, status = item
                host_set.add(project)
                get_object = self.db.objects.filter(host=host, project=project)
                if get_object:
                    get_object.update(host=host, project=project, status=status, display="1")
                else:
                    self.db.objects.create(host=host, project=project, status=status, display="1")
            db_set = { db.project for db in self.db.objects.filter(host=host) }
            diff = db_set.difference(host_set)
            print(diff, host_set, db_set)
            for diff_item in diff:
                self.db.objects.filter(project=diff_item).update(display="0")

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
    def get(self, request, format=None):
        username = request.GET.get("id", None)
        password = request.GET.get("pass", None)
        if username is None or password is None:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        try:
            Login.objects.get(username=username, password=password)
            return Response({"rest": "OK"})
        except Login.DoesNotExist:
            return Response({"rest": 0})


class AddSupervisor(SupervisorDBMixin, APIView):
    def put(self, request, format=None):
        """
          POST: { scan: 0 }
        """
        post_data = json.loads(request.body.decode())
        if post_data.get("scan", None) != 0:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        command = """/bin/bash -lc 'supervisorctl status'"""
        self.write_db(command)
        finally_result = list(self.db.objects.filter(display="1").values())
        return Response(finally_result)

    def post(self, request, format=None):
        post_data = json.loads(request.body.decode()) 
        host = post_data.get("host", None)
        project = post_data.get("project", None)
        name = post_data.get("name", None)
        describe = post_data.get("describe", None)
        self.db.objects.filter(host=host, project=project).update(name=name, describe=describe)
        finally_result = list(self.db.objects.filter(display="1").values())
        return Response(finally_result)


    def get(self, request, format=None):
        finally_result = list(self.db.objects.filter(display="1").values())
        return Response(finally_result)
        

class ControlSupervisor(SupervisorDBMixin, APIView):
    def post(self, request, format=None):
        post_data = json.loads(request.body.decode())
        hosts = post_data.get("host", None)
        action = post_data.get("action", None)
        project = post_data.get("project", None)
        print(hosts, action, project)
        if hosts is None or action is None or project is None:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
        command = """/bin/bash -lc 'supervisorctl {action} {project}'""".format(action=action, project=project)
        self.write_db(command, hosts)
        return Response({"rest": 0})
