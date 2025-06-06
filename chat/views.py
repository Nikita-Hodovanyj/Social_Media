from django.shortcuts import render
from django.views.generic.base import TemplateView

class ChatPageView(TemplateView):
    template_name = 'chat.html'