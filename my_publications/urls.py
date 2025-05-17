from django.urls import path
from .views import PublicationsView, CreatePublicationView,DeletePostView

urlpatterns = [
    path('', PublicationsView.as_view(), name='publications'),
    path('create/', CreatePublicationView.as_view(), name='create_publication'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
]