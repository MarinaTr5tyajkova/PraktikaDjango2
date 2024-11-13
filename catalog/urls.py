from django.urls import path
from . import views  # Импорт представлений

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница приложения
    path('catalog/', views.catalog_view, name='catalog'),  # Страница каталога
    path('register/', views.register, name='register'),  # Маршрут для регистрации
    path('login/', views.custom_login, name='login'),  # URL для страницы входа
    path('logout/', views.custom_logout, name='logout'),  # URL для выхода




]