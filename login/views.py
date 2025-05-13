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


# Створюємо клас представлення, який відображає форму 
class RegistrationView(FormView):

    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/login/auth/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_header'] = True
        return context

    template_name = 'registration.html'  # Шаблон форми реєстрації
    form_class = RegistrationForm        # Клас форми
    success_url = '/login/auth/'         # Куди перенаправити після успішної реєстрації


    # Метод, який викликається, якщо форма валідна
    def form_valid(self, form):

        # Отримання даних з форми
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        confirm_code = form.cleaned_data.get('confirm_code')  # без ошибки, если пусто

        code = str(random.randint(100000, 999999))


        confirm_code = form.cleaned_data['confirm_code']

        # Генерація випадкового 6-значного коду
        code = str(random.randint(100000, 999999))

        # Перевірка, чи вже існує користувач з таким email

        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Користувач з таким email вже існує!')
            # Повертаємо форму без збережень
            return self.form_invalid(form)


        
        
        
         # Перевірка, чи паролі збігаються
        if password != confirm_password:
                form.add_error('confirm_password', 'Паролі не співпадають!')
                return self.form_invalid(form)
       

        # Якщо код підтвердження ще не введено
        if not confirm_code:
            
            """
            Примітка: Якщо використовувати функцію create, 
            то вона просто додає новий об'єкт. І якщо буде спроба на створення нового об'єкта, який вже існує
            та в нього unique = True, то виведе Integrity error.
             
            Натомість, update_or_create спочатку шукає чи існує такий об'єкт чи ні
            Якщо такий є - оновлює, якщо немає - створює.
            Таким чином, цей метод обходить Integrity error.

            """
            # Збереження коду в базі даних
            ConfirmCode.objects.update_or_create(
                email=email, #  Якщо такий вже існує
                defaults={'confirm_code': code} # Вказуємо, що оновлюємо, а саме код підтвердження
            )


            # Надсилання коду підтвердження на email
            send_mail(

                subject='Код підтвердження реєстрації WORLD.IT Messenger',
                message=f'Ваш код підтвердження реєстрації: {code} ',

                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            # Відображення форми з полем для вводу коду
            return render(
                request=self.request,
                template_name=self.template_name,

                context={'form': form, 'show_code': True, 'hide_header': True}
            )
        


        else:
            # Отримуємо об’єкт моделі ConfirmCode, у якого поле email дорівнює введеному користувачем email
            saved_code = ConfirmCode.objects.get(email=email)
            if saved_code.confirm_code != confirm_code:
                form.add_error('confirm_code', 'Неправильний код підтвердження.')

                return self.form_invalid(form)



            # В інакшому випадку створюємо нового користувача
            User.objects.create_user(username=email, email=email, password=password)
            # Видаляємо код
            saved_code.delete()

            # Звертаємось до батьківського класу FormView, зберігаємо форму та перенаправляємо на success_url
            return super().form_valid(form)


       




        


    
def render_auth(request):
    form = RegistrationForm()
    if request.method == "POST": 
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

