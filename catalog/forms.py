from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import Application



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



class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']
        # widgets = {'category':  forms.CheckboxSelectMultiple()}

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.size > 2 * 1024 * 1024:  # Проверка на максимальный размер 2 Мб
            raise forms.ValidationError("Размер файла не должен превышать 2 Мб.")
        return photo

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        application = super().save(commit=False)
        if self.user:
            application.creator = self.user

        if commit:
            application.save()
            self.save_m2m()
        return application

class CaptchaForm(forms.Form):
    captcha_answer = forms.IntegerField(label='2 + 2 * 2 = ')

    def clean_captcha_answer(self):
        answer = self.cleaned_data.get('captcha_answer')
        if answer != 6:  # Проверка правильного ответа
            raise ValidationError("Неправильный ответ на капчу. Попробуйте снова.")
        return answer

