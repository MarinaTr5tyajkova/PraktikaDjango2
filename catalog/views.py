from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm
from .forms import CustomLoginForm
from django.shortcuts import render, redirect
from .forms import ApplicationForm
from django.views.generic import TemplateView
from .models import Application


class SuccessView(TemplateView):
    template_name = "success.html"

class IndexView(View):
    def get(self, request):
        # Получаем только заявки со статусом 'done'
        applications = Application.objects.filter(status='done')
        form = ApplicationForm()  # Создаем экземпляр формы
        return render(request, 'index.html', {'applications': applications, 'form': form})

    def post(self, request):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Сохранение заявки в базу данных
            return redirect('success')  # Перенаправление на страницу успеха
        applications = Application.objects.filter(status='done')  # Получаем заявки снова для отображения
        return render(request, 'index.html', {'applications': applications, 'form': form})

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Учетная запись успешно создана! Вы можете войти в систему.')
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
        return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Укажите путь к вашему шаблону
    form_class = CustomLoginForm  # Укажите вашу кастомную форму

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли в систему!")  # Сообщение об успешном входе
        return super().form_valid(form)

class CustomLogoutView(View):
    def post(self, request):
        logout(request)  # Выход пользователя
        messages.success(request, 'Вы успешно вышли из системы!')  # Сообщение об успешном выходе
        return render(request, 'registration/logout_success.html')  # Отображение шаблона выхода

    def get(self, request):
        return render(request, 'registration/logout_success.html')  # Или можно перенаправить на главную страницу

class CreateApplicationView(View):
    def get(self, request):
        form = ApplicationForm()
        return render(request, 'create_application.html', {'form': form})

    def post(self, request):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Сохранение заявки в базу данных
            return redirect('success')  # Перенаправление на страницу успеха
        return render(request, 'create_application.html', {'form': form})



