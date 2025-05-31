from django.urls import path
from .views import *

urlpatterns = [
    path('personal_info/', PersonalInfoPage.as_view(), name = 'personal_info'),
    path('albums/', AlbumsPage.as_view(), name = 'albums')
]