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




class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/login/auth/'  # Адрес для редиректа после успешной регистрации

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'hide_header': True  # Скрыть хедер при первом заходе
        })

    def post(self, request, *args, **kwargs):
        # Проверка: был ли введён код
        show_code = any(request.POST.get(f'code{i}', '') for i in range(1, 7))

        if not show_code:
            # Первый этап: регистрация и отправка кода
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Генерируем код
                code = str(random.randint(100000, 999999))
                if email:
                    ConfirmCode.objects.update_or_create(email=email, defaults={'confirm_code': code})

                # Отправляем письмо
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
                    'password': password,
                    'hide_header': True  # Скрываем хедер при вводе кода
                })
            else:
                return self.form_invalid(form)

        else:
            # Второй этап: проверка кода и создание пользователя
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
                    'code_error': 'Код підтвердження не знайдено.',
                    'hide_header': True
                })

            if saved.confirm_code != code_input:
                return render(request, self.template_name, {
                    'show_code': True,
                    'email': email,
                    'password': password,
                    'code_error': 'Невірний код підтвердження.',
                    'hide_header': True
                })

            # Создаём пользователя
            User.objects.create_user(username=email, email=email, password=password)
            saved.delete()

            return redirect(self.success_url)


    
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
