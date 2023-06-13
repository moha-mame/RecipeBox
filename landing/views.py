from django.shortcuts import render,redirect
from django.views.generic import TemplateView




# Create your views here.class landing_page(TemplateView):
class landing_page(TemplateView):
    context = {}
    template_name = 'landing/index.html'

class Home(TemplateView):
    context = {}
    template_name = 'home/home.html'