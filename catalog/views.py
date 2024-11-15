from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from .models import Application
from .forms import UserRegisterForm, LoginForm, ApplicationForm, CaptchaForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.contrib.auth import login
from django.shortcuts import redirect





class SuccessView(TemplateView):
    template_name = "catalog/success.html"

class SuccessCaptchaView(TemplateView):
    template_name = "success_captcha.html"


class IndexView(View):
    def get(self, request):
        # Получаем только заявки со статусом 'done'
        applications = Application.objects.filter(status='done')
        completed_requests = Application.objects.filter(status='completed')
        accepted_requests_count = Application.objects.filter(status='in_progress').count()
        form = ApplicationForm()  # Создаем экземпляр формы

        return render(request, 'index.html', {
            'applications': applications,
            'completed_requests': completed_requests,
            'accepted_requests_count': accepted_requests_count,
            'form': form,
            'non_deletable_statuses': ['in_progress', 'completed']  # Передавать статусы в качестве контекста
        })

    def post(self, request):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Assign current user to the application
            application.save()
            return redirect('success_captcha')  # Перенаправление на страницу успеха

        # Если форма недействительна, повторно выберите приложения для отображения
        applications = Application.objects.filter(status='done')  # Снова показывать только "завершенные" приложения
        completed_requests = Application.objects.filter(status='completed')
        accepted_requests_count = Application.objects.filter(status='in_progress').count()

        return render(request, 'index.html', {
            'applications': applications,
            'completed_requests': completed_requests,
            'accepted_requests_count': accepted_requests_count,
            'form': form,
            'non_deletable_statuses': ['in_progress', 'completed']  # Передавать статусы в качестве контекста
        })



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # Проверка на одобрение пользователя
                if user.is_approved:
                    login(request, user)
                    return redirect('index')  # Перенаправление на главную страницу или другую страницу
                else:
                    messages.error(request, "Ваша учетная запись не одобрена администратором.")
                    return render(request, 'registration/login.html', {'form': form})

            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})



class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        captcha_form = CaptchaForm()  # Создание формы капчи
        return render(request, 'registration/register.html', {'form': form, 'captcha_form': captcha_form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        captcha_form = CaptchaForm(request.POST)  # Получение данных формы капчи

        # Проверка обеих форм на валидность
        if form.is_valid() and captcha_form.is_valid():
            form.save()  # Сохранение пользователя в базе данных
            messages.success(request, 'Учетная запись успешно создана! Вы можете войти в систему.')
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации

        # Если одна из форм не валидна, отобразите их снова
        return render(request, 'registration/register.html', {'form': form, 'captcha_form': captcha_form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Укажите путь к вашему шаблону
    form_class = LoginForm  # Укажите вашу кастомную форму

    def form_valid(self, form):
        user = form.get_user()  # Получаем пользователя из формы
        if not user.is_approved:
            messages.error(self.request, "Ваша учетная запись не одобрена администратором.")
            return self.form_invalid(form)  # Возвращаем ошибку, если пользователь не одобрен

        login(self.request, user)  # Вход пользователя
        messages.success(self.request, "Вы успешно вошли в систему!")  # Сообщение об успешном входе
        return super().form_valid(form)  # Выполняем стандартную логику

class CustomLogoutView(View):
    def post(self, request):
        logout(request)  # Выход пользователя
        messages.success(request, 'Вы успешно вышли из системы!')  # Сообщение об успешном выходе
        return render(request, 'registration/logout_success.html')  # Отображение шаблона выхода

    def get(self, request):
        return render(request, 'registration/logout_success.html')  # Или можно перенаправить на главную страницу

class CreateApplicationView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('registration/login')  # Redirect to login if not authenticated
        form = ApplicationForm(user=request.user)
        return render(request, "catalog/create_application.html", {'form': form})  # Make sure the path matches

    def post(self, request):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Assign current user to the application
            application.save()
            return redirect('success')  # Redirect to success page
        form = ApplicationForm(user=request.user)
        return render(request, "catalog/create_application.html", {'form': form})  # Ensure path matches here too

class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = 'catalog/delete_confirmation.html'
    context_object_name = 'application'
    success_url = reverse_lazy('index')  # Redirect to the index page after deletion

    def get_object(self, queryset=None):
        """Override to ensure the user can only delete their own applications."""
        obj = super().get_object(queryset)
        if self.request.user != obj.creator:
            messages.error(self.request, "Вы не можете удалить эту заявку.")
            raise PermissionDenied  # Raise an error if the user is not the owner
        if obj.status in ['in_progress', 'completed']:
            messages.error(self.request, "Эту заявку нельзя удалить.")
            raise PermissionDenied  # Raise an error if the status does not allow deletion
        return obj

    def post(self, request, *args, **kwargs):
        """Override post method to show success message after deletion."""
        messages.success(request, "Заявка успешно удалена.")
        return super().post(request, *args, **kwargs)

class AccountListView(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'catalog/personal_account.html'

    def get_queryset(self):
        return Application.objects.filter(creator=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['designapplication_list'] = self.get_queryset()
        print("Current user:", self.request.user)  # Debugging output
        return context


class AppDelete(DeleteView):
    model = Application
    template_name = 'delete_application.html'
    success_url = reverse_lazy('personal_account')

    def get_queryset(self):
        return Application.objects.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()  # Ensure the object is available in the context
        return context