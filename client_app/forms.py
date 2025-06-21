from django import forms
from django.contrib.auth.models import User
from . import models
from admin_app import models
from django.contrib.auth import authenticate

class ClientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ['first_name', 'last_name', 'mobile', 'email', 'address']

class LoginForm(forms.Form):
    username = forms.CharField(label='Псевдоним')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Неверный псевдоним или пароль')
        return cleaned_data