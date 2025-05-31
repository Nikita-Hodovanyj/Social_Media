from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    TAG_CHOICES = [
        ('music', 'Музика'),
        ('vacation', 'Відпочинок'),
        ('inspiration', 'Натхнення'),
        ('life', 'Життя'),
        ('travel', 'Подорожі'),
        ('nature', 'Природа'),
        ('harmony', 'Гармонія'),
        ('movies', 'Фільми'),
        ('reading', 'Читання'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        ('calm', 'Спокій'),
        
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    topic = models.CharField(max_length=255, verbose_name="Тема")
    tags = models.CharField(max_length=255, blank=True) 
    text = models.TextField(verbose_name="Текст")
    link = models.CharField(max_length=255, blank=True, verbose_name="Ссылка")
    image = models.ImageField(upload_to='images/posts/', verbose_name="Изображение")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_tags_list(self):
        """Возвращает список выбранных тегов"""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/posts')