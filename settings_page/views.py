from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class PersonalInfoPage(TemplateView):
    template_name = 'personal_info.html'

class AlbumsPage(TemplateView):
    template_name = 'albums.html'