from rest_framework import serializers
from .models import *


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ('id', 'username', 'password', 'create_time', 'last_login_time')

class RemoteHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteHost
        fields = ('id', 'ip', 'hostname', 'alias_name', 'supervisor_project')


class JobMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMessage
        field = ('id', 'job_id', 'message')


class RemoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remote
        field = ('id', 'host_id', 'login', 'passwd', 'port')
