from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm
from .forms import CustomLoginForm
from .models import DesignRequest
from .forms import DesignRequestForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

def index(request):
    return render(request, 'index.html')

"""
class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # Получаем завершенные запросы
        completed_requests = DesignRequest.objects.filter(status='completed').order_by('-timestamp')[:4]
        # Получаем количество запросов в процессе выполнения
        in_progress_count = DesignRequest.objects.filter(status='in_progress').count()

        # Формируем контекст для шаблона
        context = {
            'completed_requests': completed_requests,
            'in_progress_count': in_progress_count,
        }

        # Возвращаем рендеринг шаблона с контекстом
        return render(request, self.template_name, context)
"""

class CatalogView(View):
    def get(self, request):
        return render(request, 'catalog/catalog.html')  # Отображение страницы каталога

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

class CreateDesignRequestView(CreateView):
    model = DesignRequest
    form_class = DesignRequestForm
    template_name = 'create_design_request.html'
    success_url = reverse_lazy('view_requests')

    def form_valid(self, form):
        design_request = form.save(commit=False)
        design_request.user = self.request.user  # Associate the request with the logged-in user
        design_request.save()
        return super().form_valid(form)

class ViewRequestsView(ListView):
    model = DesignRequest
    template_name = 'view_requests.html'
    context_object_name = 'requests'

    paginate_by = 4

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user)  # Get requests for the logged-in user


