from django.urls import path
from .views import PersonalInfoPage, AlbumsPage, UpdateUserInfoView

urlpatterns = [
    path('personal_info/', PersonalInfoPage.as_view(), name='personal_info'),
    path('albums/', AlbumsPage.as_view(), name='albums'),
    path('update_user_info/', UpdateUserInfoView.as_view(), name='update_user_info'),
]


