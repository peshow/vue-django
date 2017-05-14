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
        username = request.GET.get("id")
        password = request.GET.get("pass")
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
            SupervisorHost.objects.update_or_create(ip=host, supervisor_project=",".join(supervisor_project))

        set_host = set(scan_result)
        set_SupervisorHost_host = {i['ip'] for i in SupervisorHost.objects.values()}
        diff = set_SupervisorHost_host.difference(set_host)
        assert diff
        for ip in diff:
            SupervisorHost.objects.delete(ip)
        return Response(scan_result)
            
    def get(self, request, format=None):
        remote = list(SupervisorHost.objects.values())
        return Response(remote)
        
