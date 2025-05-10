from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from Social_Media.settings import EMAIL_HOST_USER
from .forms import RegistrationForm

from Social_Media.settings import EMAIL_HOST_USER

from .models import ConfirmCode
import random

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/login/auth/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_header'] = True
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        confirm_code = form.cleaned_data.get('confirm_code')  # без ошибки, если пусто

        code = str(random.randint(100000, 999999))

        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Користувач з таким email вже існує!')
            return self.form_invalid(form)

        if not confirm_code:
            if password != confirm_password:
                form.add_error('confirm_password', 'Паролі не співпадають!')
                return self.form_invalid(form)

            ConfirmCode.objects.update_or_create(email=email, defaults={'confirm_code': code})

            send_mail(
                subject='Код підтвердження реєстрації WORLD.IT Messenger',
                message=f'Ваш код підтвердження реєстрації: {code}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return render(
                request=self.request,
                template_name=self.template_name,
                context={'form': form, 'show_code': True, 'hide_header': True}
            )
        else:
            try:
                saved_code = ConfirmCode.objects.get(email=email)
            except ConfirmCode.DoesNotExist:
                form.add_error('confirm_code', 'Код підтвердження не знайдено.')
                return self.form_invalid(form)

            if saved_code.confirm_code != confirm_code:
                form.add_error('confirm_code', 'Неправильний код підтвердження.')
                return self.form_invalid(form)

            # Створення користувача
            User.objects.create_user(username=email, email=email, password=password)
            saved_code.delete()

            return super().form_valid(form)

       




        


    
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
