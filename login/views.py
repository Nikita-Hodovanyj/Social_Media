from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from Social_Media.settings import EMAIL_HOST_USER
from .forms import RegistrationForm

from Social_Media.settings import EMAIL_HOST_USER

from .models import ConfirmCode

import random

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



import random, os

from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from .forms import RegistrationForm
from .models import ConfirmCode
import random


import random
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from .models import ConfirmCode
from .forms import RegistrationForm

class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/authorizatio.html'

    def post(self, request, *args, **kwargs):
        show_code = any(request.POST.get(f'code{i}', '') for i in range(1, 7))

        if not show_code:
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                code = str(random.randint(100000, 999999))
                ConfirmCode.objects.update_or_create(email=email, defaults={'confirm_code': code})

                send_mail(
                    'Код підтвердження',
                    f'Ваш код підтвердження: {code}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )

                return render(request, self.template_name, {
                    'show_code': True,
                    'email': email,
                    'password': password
                })
            else:
                return self.form_invalid(form)
        else:
            # Получаем данные из скрытых полей
            email = request.POST.get('email')
            password = request.POST.get('password')
            code_input = ''.join([request.POST.get(f'code{i}', '') for i in range(1, 7)])

            try:
                saved = ConfirmCode.objects.get(email=email)
            except ConfirmCode.DoesNotExist:
                return render(request, self.template_name, {
                    'show_code': True,
                    'email': email,
                    'password': password,
                    'code_error': 'Код підтвердження не знайдено.'
                })

            if saved.confirm_code != code_input:
                return render(request, self.template_name, {
                    'show_code': True,
                    'email': email,
                    'password': password,
                    'code_error': 'Невірний код підтвердження.'
                })

            # Создаём пользователя
            User.objects.create_user(username=email, email=email, password=password)
            saved.delete()
            return super().form_valid(self.get_form())



    
def render_auth(request):
    form = RegistrationForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            messages.error(request, 'Невірний email або пароль.')

    return render(request, 'authorization.html', {'form': form, 'hide_header': True}) 

def logout_user(request):
    logout(request)
    print(f'{request.user.username} Logout')
    return redirect('auth')

