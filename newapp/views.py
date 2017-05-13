from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class VueNew(TemplateView):
    template_name = "newapp/index.html"
