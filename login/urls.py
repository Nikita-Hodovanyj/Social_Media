from django.urls import path
from .views import * 
from .views import EmailBackend
from .views import render_auth
urlpatterns = [
    
    
    path('auth/', render_auth, name='auth'),
    path('reg/' ,view = RegistrationView.as_view(), name = "reg"),
    path('logout/', view=logout_user, name = 'logout')

]   