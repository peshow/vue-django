import os
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
    def check_get(self, *args):
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


class AddSupervisor(APIView):
    def post(self, request, format=None):
        playrun = PlayRun()
        scan_result = playrun.run([("shell", """/bin/bash -lc 'supervisorctl status'""")], hosts="all_user")
        for host, supervisor_project in scan_result:
            SupervisorHost.objects.update_or_create(ip=host, project=",".join(supervisor_project))

        # 取扫描结果与数据库内容的差集
        set_host = set(scan_result)
        set_SupervisorHost_host = {(dataElement['ip'], dataElement['project']) for dataElement in SupervisorHost.objects.values()}
        diff = set_SupervisorHost_host.difference(set_host)
        assert diff
        for ip in diff:
            SupervisorHost.objects.delete(ip)
        return Response(scan_result)
            
    def get(self, request, format=None):
        remote = list(RemoteHost.objects.values())
        test = [{"ip": "172.16.20.120", "project": "sogou:sogou1", "message": "This is message", "status": "RUNNING"}]
        print("fdsfasdf")
        return Response(test)
        

class ControlSupervisor(APIView):
    def get(self, request, format=None):
        ip = request.GET.get("ip", None)
        action = request.GET.get("action", None)
        project = request.GET.get("project", None)
        if ip is None or action is None or project is None:
            return Response("Bad request!", status=status.HTTP_400_BAD_REQUEST)
#        play = PLayRun()
#        scan_result = playrun.run([("shell", """/bin/bash -lc 'supervisorctl {action} {project}'""".format(action=action, project=project))], hosts=ip)
        return Response({"rest": 0})
