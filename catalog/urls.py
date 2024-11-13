from django.urls import path
from . import views
from .views import CatalogView, RegisterView, CustomLoginView, CustomLogoutView
from .views import CreateDesignRequestView, ViewRequestsView
# from .views import IndexView

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница приложения
    path('catalog/', CatalogView.as_view(), name='catalog'),  # Страница каталога
    path('register/', RegisterView.as_view(), name='register'),  # Маршрут для регистрации
    path('login/', CustomLoginView.as_view(), name='login'),  # URL для страницы входа
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # URL для выхода
    path('create/', CreateDesignRequestView.as_view(), name='create_design_request'),
    path('requests/', ViewRequestsView.as_view(), name='view_requests'),

]
