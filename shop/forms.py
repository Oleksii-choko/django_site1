from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Пароль'}))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widget = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}) }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Імя')
    email = forms.EmailField(label='Почта')
    subject = forms.CharField(max_length=100, label='Тема')
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Ваше сообщение...'}),
                              label='Сообщение')

