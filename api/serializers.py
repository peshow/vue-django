from rest_framework import serializers
from .models import *


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ('id', 'username', 'password', 'create_time', 'last_login_time')

class SupervisorHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorHost
        fields = ('id', 'name', 'ip', 'hostname', 'supervisor_project')


class JobMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMessage
        field = ('id', 'job_id', 'message')

class JobServializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        field = ('id', 'remote_id', 'jobname', 'command')


class RemoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remote
        field = ('id', 'name', 'ip', 'host', 'user', 'port', 'default_path', 'create_time')
