from django.db import models

# Create your models here.


class ConfirmCode(models.Model):
    email = models.EmailField(unique=True)
    confirm_code = models.CharField(max_length=6)
    
