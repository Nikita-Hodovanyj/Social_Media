from django.db import models

class ConfirmCode(models.Model):
    email = models.EmailField(unique=True)
    confirm_code = models.CharField(max_length=6)
