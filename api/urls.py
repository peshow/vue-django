from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^manager/', include([
        url(r'codeChange/$', CodeChange.as_view(), name="codeChange")
    ])),
    url(r'remote/', include([
        url(r'get/$', Upload.as_view(), name="remote_upload")
    ])),
    url(r'login/', include([
        url(r'get/$', LoginAPI.as_view(), name="login")
    ])),
    url(r'supervisor/', AddSupervisor.as_view(), name="supervisor")
]
