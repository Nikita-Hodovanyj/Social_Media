from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from Social_Media.settings import EMAIL_HOST_USER
from .forms import RegistrationForm
from .models import ConfirmCode
import random


# Create your views here.

class RegistrationView(FormView):
    template_name = 'registration.html'  
    form_class = RegistrationForm  
    success_url = '/login/auth/'


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        confirm_code = form.cleaned_data['confirm_code']
        
        code = str(random.randint(100000, 999999))



        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Користувач з таким email вже існує!')
            return self.form_invalid(form)
        

        if not confirm_code:

            if password != confirm_password:
                form.add_error('confirm_password', 'Паролі не співпадають!')
                return self.form_invalid(form)
            

            ConfirmCode.objects.update_or_create(email = email, defaults= {'confirm_code':code})

            send_mail(
                subject='Код підтвердження реєстрації WORLD.IT Messenge`r',
                message= f'Ваш код підтвердження реєстрації: {code} ',
                from_email = EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return render(
                request=self.request, 
                template_name= self.template_name, 
                context={'form': form,'show_code': True, }
            )
        
        else:
            
            saved_code = ConfirmCode.objects.get(email=email)

            if saved_code.confirm_code != confirm_code:
                form.add_error('confirm_code', 'Неправильний код підтвердження.')
                # return render(
                #     request=self.request, 
                #     template_name= self.template_name, 
                #     context={'show_code': True, }
                # )

            # Створення користувача
            User.objects.create_user(username=email, email=email, password=password)
            saved_code.delete()

            return super().form_valid(form)




        


    
class AuthorizaView(TemplateView):
    template_name = "authorization.html"