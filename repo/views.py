from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class VueWeb(TemplateView):
    template_name = 'repo/index.html'


class Attribute(TemplateView):
    template_name = 'repo/a.html'


class Computed(TemplateView):
    template_name = 'repo/b.html'


class LoginBase(TemplateView):
    template_name = 'repo/login.html'
