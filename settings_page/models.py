from django.db import models

# Create your models here.
from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    year = models.IntegerField()
    is_hidden = models.BooleanField(default=False)  # 👁 флаг приховування

    def __str__(self):
        return f"{self.name} ({self.year})"
    
from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Можно добавить связь с пользователем или альбомом

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username
class OnePhoto(models.Model):
    photo = models.ImageField(upload_to='one_photos/')

