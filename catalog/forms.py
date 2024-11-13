from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm
from .models import DesignRequest

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),  # Добавляем класс Bootstrap
        error_messages={
            'required': 'Email обязателен для заполнения.',
            'invalid': 'Введите корректный email адрес.'
        }
    )

    full_name = forms.CharField(
        label='ФИО',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),  # Добавляем класс Bootstrap
        error_messages={
            'required': 'ФИО обязательно для заполнения.'
        }
    )

    username = forms.CharField(
        label='Логин',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),  # Добавляем класс Bootstrap
        error_messages={
            'required': 'Логин обязателен для заполнения.'
        }
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # Добавляем класс Bootstrap
        required=True
    )

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # Добавляем класс Bootstrap
        required=True
    )

    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        error_messages={
            'required': 'Необходимо согласие на обработку персональных данных.'
        }
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2', 'consent']

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллические буквы, пробелы и дефисы.')
        return full_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9\-]+$', username):
            raise ValidationError('Логин должен содержать только латиницу, цифры и дефисы.')

        # Проверка уникальности логина
        if User.objects.filter(username=username).exists():
            raise ValidationError('Этот логин уже занят.')

        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Класс Bootstrap для стилизации
            'placeholder': 'Введите логин или email'  # Подсказка для пользователя
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Класс Bootstrap для стилизации
            'placeholder': 'Введите пароль'  # Подсказка для пользователя
        })
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Класс Bootstrap для стилизации
            'placeholder': 'Введите логин или email'  # Подсказка для пользователя
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Класс Bootstrap для стилизации
            'placeholder': 'Введите пароль'  # Подсказка для пользователя
        })
    )


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 2MB)
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("The maximum file size is 2MB.")
            return image
        raise forms.ValidationError("This field is required.")