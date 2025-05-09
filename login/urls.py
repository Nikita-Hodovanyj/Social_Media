from django.urls import path
from .views import * 

urlpatterns = [
    
    path('auth/',view=AuthorizaView.as_view(), name="auth" ),
    path('reg/' ,view = RegistrationView.as_view(), name = "reg")

]