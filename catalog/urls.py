from django.urls import path
from django.conf import settings
from .views import RegisterView, CustomLoginView, CustomLogoutView, SuccessView, AccountListView
from .views import CreateApplicationView
from .views import IndexView
from django.conf.urls.static import static
from .views import ApplicationDeleteView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('success/', SuccessView.as_view(), name='success'),
    path('register/', RegisterView.as_view(), name='register'),  # Маршрут для регистрации
    path('login/', CustomLoginView.as_view(), name='login'),  # URL для страницы входа
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # URL для выхода
    path('create_application/', CreateApplicationView.as_view(), name='create_application'),
    path('personal_account/', AccountListView.as_view(), name='personal_account'),
    path('application/delete/<int:pk>/', ApplicationDeleteView.as_view(), name='delete_application'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

