from django import forms


class ModalActionForm(forms.Form):
    name = forms.CharField(label='Ім’я', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введіть Ваше ім’я'}))
    surname = forms.CharField(label='Прізвище', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введіть Ваше прізвище'}))
    login = forms.CharField(label='Ім’я користувача', max_length=50, widget=forms.TextInput(attrs={'placeholder': '@'}))

    def clean_login(self):
        login = self.cleaned_data['login']
        if not login.startswith('@'):
            login = '@' + login
        return login