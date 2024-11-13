from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from .forms import LoginForm
from django.contrib.auth import logout



def index(request):
    return render(request, 'index.html')  # Отображение главной страницы

def catalog_view(request):
    return render(request, 'catalog/catalog.html')  # Отображение страницы каталога

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Учетная запись успешно создана! Вы можете войти в систему.')  # Add success message
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Передаем данные формы
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Аутентификация пользователя
            if user is not None:
                login(request, user)  # Вход пользователя
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('index')  # Перенаправление на главную страницу после успешного входа
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()  # Пустая форма для GET запроса

    return render(request, 'registration/login.html', {'form': form})  # Отображение формы

def custom_logout(request):
    logout(request)  # Выход пользователя
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('index')  # Перенаправление на главную страницу



