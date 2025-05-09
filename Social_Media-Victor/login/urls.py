from django.urls import path
from .views import * 

urlpatterns = [
    
    path('aut/',view=AuthorizaView.as_view(), name="aut" ),
    path('reg/' ,view = RegistrationView.as_view(), name = "reg")

]
