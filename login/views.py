from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.

class RegistrationView(TemplateView):
    template_name = "registration.html"

    
class AuthorizaView(TemplateView):
    template_name = "authorization.html"