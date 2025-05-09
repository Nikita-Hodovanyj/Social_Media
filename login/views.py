from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .forms import RegistrationForm
from Social_Media.settings import EMAIL_HOST_USER

# Create your views here.

class RegistrationView(FormView):
    template_name = 'registration.html'  
    form_class = RegistrationForm  
    success_url = '/login/reg/'


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Користувач з таким email вже існує!')
            return self.form_invalid(form)
        
        if password == confirm_password:
            User.objects.create_user(username = email, email = email, password = password)

            send_mail(
                subject='Код підтвердження реєстрації',
                message='Ваш код підтвердження реєстрації:  123',
                from_email= EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return super().form_valid(form)

    

        

        






    
class AuthorizaView(TemplateView):
    template_name = "authorization.html"