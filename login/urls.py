from django.urls import path
from .views import * 

urlpatterns = [
    
    path('auth/',view=render_auth, name="auth" ),
    path('reg/' ,view = RegistrationView.as_view(), name = "reg"),
    path('logout/', view=logout_user, name = 'logout')

]