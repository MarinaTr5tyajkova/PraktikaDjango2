from django.urls import path
from django.conf import settings
from .views import RegisterView, CustomLoginView, CustomLogoutView, SuccessView
from .views import CreateApplicationView
from .views import IndexView
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('success/', SuccessView.as_view(), name='success'),
    path('register/', RegisterView.as_view(), name='register'),  # Маршрут для регистрации
    path('login/', CustomLoginView.as_view(), name='login'),  # URL для страницы входа
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # URL для выхода
    path('create-application/', CreateApplicationView.as_view(), name='create_application'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

