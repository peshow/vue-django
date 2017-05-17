from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^manager/', include([
        url(r'^codeChange/$', CodeChange.as_view(), name="codeChange")
    ])),
    url(r'remote/', include([
        url(r'^get/$', Upload.as_view(), name="remote_upload")
    ])),
    url(r'login/', include([
        url(r'^$', LoginAPI.as_view(), name="login")
    ])),
    url(r'supervisor/', include([
        url(r'^$', SupervisorAPI.as_view(), name="supervisor"),
        url(r'^(?P<rest_id>\d+)$', SupervisorAPI.as_view(), name="supervisor_not_params"),
        url(r'^(?P<rest_id>\d+)/action/$', SupervisorAction.as_view())
    ])),
    url(r'crontab/', include([
        url(r'^$', CrontabAPI.as_view(), name="crontab_not_params"),
        url(r'^(?P<rest_id>\d+)$', CrontabAPI.as_view(), name="crontab"),
        url(r'^(?P<rest_id>\d+)$/action/$', CrontabAction.as_view(), name="crontab"),
    ]))
#    url(r'supervisor/$', AddSupervisor.as_view(), name="supervisor"),
#    url(r'supervisor/control/$', ControlSupervisor.as_view())
]
