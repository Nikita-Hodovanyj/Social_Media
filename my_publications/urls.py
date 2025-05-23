from django.urls import path
from .views import PublicationsView, CreatePublicationView,DeletePostView,EditPostView

urlpatterns = [
    path('', PublicationsView.as_view(), name='publications'),
    path('create/', CreatePublicationView.as_view(), name='create_publication'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('edit/<int:pk>/', EditPostView.as_view(), name='edit_post')
]