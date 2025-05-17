from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    name = models.CharField(max_length=255)
    topic =  models.CharField(max_length=255)
    text = models.TextField()
    link =  models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/posts')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True,blank=True, verbose_name='Автор')
    def __str__(self):
        return self.name