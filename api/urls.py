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
        url(r'^$', AddSupervisor.as_view(), name="supervisor"),
        url(r'^control/$', ControlSupervisor.as_view())
    ])),
    url(r'crontab/', include([
        url(r'^$', CrontabAPI.as_view(), name="crontab")
    ]))
#    url(r'supervisor/$', AddSupervisor.as_view(), name="supervisor"),
#    url(r'supervisor/control/$', ControlSupervisor.as_view())
]
