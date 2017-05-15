from django.db import models

# Create your models here.
class SupervisorHost(models.Model):
    ip = models.CharField(max_length=100, blank=False)
    project = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="空")
    status = models.CharField(max_length=45, default="")
    describe = models.TextField(max_length=200, default="")


class Remote(models.Model):
    name = models.CharField(max_length=200, default="")
    ip = models.CharField(max_length=100, default="")
    host = models.CharField(max_length=100, default="")
    user = models.CharField(max_length=45, default="")
    port = models.IntegerField(default=22)
    default_path = models.CharField(max_length=200, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    

class Job(models.Model):
    remote_id = models.ForeignKey(Remote)
    jobname = models.CharField(max_length=45, blank=False)
#    item = models.CharField(max_length=45, default="")
#    item_path = models.CharField(max_length=45, default="")
    command = models.CharField(max_length=300, default="")
    

class JobMessage(models.Model):
    job_id = models.ForeignKey(Job)
    message = models.TextField(max_length=100, default="")


class Login(models.Model):
    username = models.CharField(max_length=45, blank=False)
    password = models.CharField(max_length=45, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now=True)
  
    class Meta:
        unique_together = ('username', 'password')


class System(models.Model):
    ssh_key_path = models.CharField(max_length=100, default="/root/.ssh/id_rsa")
