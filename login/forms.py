from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Електронна пошта", max_length=255, widget = forms.EmailInput)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Підтверди пароль", widget=forms.PasswordInput)
    confirm_code = forms.CharField(label = 'Підтверди код реєстрації', max_length=6, widget = forms.TextInput(attrs= {'id': 'regInput'}), required= False)