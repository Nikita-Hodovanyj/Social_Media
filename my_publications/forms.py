from django import forms
from .models import Post

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["name", "topic", "text", "link", "image"]
        labels = {
            'name': 'Назва публікації',
            'topic': 'Тема публікації',
            'text': '',
            'link': 'Посилання',
            'image': '',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-field", "placeholder": "Назва публікації"}),
            "topic": forms.TextInput(attrs={"class": "form-field", "placeholder": "Тема публікації"}),
            "text": forms.Textarea(attrs={"class": "form-textarea"}),
            "link": forms.TextInput(attrs={"class": "form-field", "placeholder": "Посилання"})
        }
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        return post