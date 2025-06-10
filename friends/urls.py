from django.urls import path
from .views import FriendsView , UserProfileView
urlpatterns = [
    path('friends/', FriendsView.as_view(), name='friends'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='user_prof'),

]