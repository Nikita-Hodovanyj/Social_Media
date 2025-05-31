from django import forms
from .models import Post


class PublicationForm(forms.ModelForm):
    TAG_CHOICES = Post.TAG_CHOICES

    tags = forms.MultipleChoiceField(
        choices=TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'vertically-scroll'
        }),
        required=False,
        label="Теги"
)

    class Meta:
        model = Post
        fields = ["name", "topic", "tags", "text", "link"]
        labels = {
            'name': 'Название публикации',
            'topic': 'Тема публикации',
            'text': '',
            'link': 'Ссылка',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-field", "placeholder": "Назвіть публікацію"}),
            "topic": forms.TextInput(attrs={"class": "form-field", "placeholder": "Придумайте тему публікації"}),
            "text": forms.Textarea(attrs={"class": "form-textarea", "placeholder": "Опишіть публікацію"}),
            "link": forms.TextInput(attrs={"class": "form-field", "placeholder": "Посилання на цікаву статтю"})
        }

    def clean_tags(self):
        """Преобразуем список тегов в строку, разделенную запятыми"""
        tags = self.cleaned_data.get('tags', [])
        return ','.join(tags) if tags else ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tags:
            self.initial['tags'] = self.instance.get_tags_list()