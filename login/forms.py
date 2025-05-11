from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, widget = forms.EmailInput)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Підтвердження паролю", widget=forms.PasswordInput)
    confirm_code = forms.CharField(label = 'Підтвердження коду реєстрації', max_length=6, widget = forms.TextInput(attrs= {'id': 'regInput'}), required= False)