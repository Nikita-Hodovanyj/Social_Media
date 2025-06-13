from django.urls import path
from .views import FriendsView, UserProfileView, send_friend_request, accept_request

urlpatterns = [
    path('friends/', FriendsView.as_view(), name='friends'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='user_prof'),
    path('send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept_request/<int:request_id>/', accept_request, name='accept_request'),
]