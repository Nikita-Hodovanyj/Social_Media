from django.db import models

class ConfirmCode(models.Model):
    email = models.EmailField(unique=True)
    confirm_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} – {self.confirm_code}'
