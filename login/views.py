# views.py

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegistrationForm
from .models import ConfirmCode
import random
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


# Кастомный backend для авторизации по email
class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None


# Регистрация с подтверждением кода
class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/login/auth/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'hide_header': True
        })

    def post(self, request, *args, **kwargs):
        show_code = any(request.POST.get(f'code{i}', '') for i in range(1, 7))

        if not show_code:
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email'].lower()
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
                    'password': password,
                    'hide_header': True
                })
            return self.form_invalid(form)

        else:
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            code_input = ''.join([request.POST.get(f'code{i}', '') for i in range(1, 7)])

            try:
                saved = ConfirmCode.objects.get(email=email)
            except ConfirmCode.DoesNotExist:
                return self._code_error(email, password, 'Код підтвердження не знайдено.')

            if saved.confirm_code != code_input:
                return self._code_error(email, password, 'Невірний код підтвердження.')

            if not User.objects.filter(username=email).exists():
                User.objects.create_user(username=email, email=email, password=password)

            saved.delete()
            return redirect(self.success_url)

    def _code_error(self, email, password, msg):
        return render(self.request, self.template_name, {
            'show_code': True,
            'email': email,
            'password': password,
            'code_error': msg,
            'hide_header': True
        })


# Авторизация
def render_auth(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Невірний email або пароль.')

    return render(request, 'authorization.html', {
        'hide_header': True
    })


# Выход из аккаунта
def logout_user(request):
    logout(request)
    return redirect('auth')
