from django.db import models

# Create your models here.
class RemoteHost(models.Model):
    ip = models.CharField(max_length=45, blank=False)
    hostname = models.CharField(max_length=45)
    alias_name = models.CharField(max_length=100)
    

class Job(models.Model):
    host_id = models.ForeignKey(RemoteHost)
    jobname = models.CharField(max_length=45, blank=False)
    item = models.CharField(max_length=45)
    item_path = models.CharField(max_length=45)
    command = models.CharField(max_length=300)
    

class JobMessage(models.Model):
    job_id = models.ForeignKey(Job)
    message = models.TextField(max_length=100)


class Remote(models.Model):
    host_id = models.ForeignKey(RemoteHost)
    login = models.CharField(max_length=45, blank=False)
    passwd = models.CharField(max_length=45)
    port = models.IntegerField()
    

class Login(models.Model):
    username = models.CharField(max_length=45, blank=False)
    password = models.CharField(max_length=45, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now=True)
  
    class Meta:
        unique_together = ('username', 'password')
