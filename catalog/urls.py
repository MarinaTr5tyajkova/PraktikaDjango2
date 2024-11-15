from django.urls import path
from django.conf import settings
from .views import RegisterView, CustomLogoutView, SuccessView, AccountListView, login_user
from .views import CreateApplicationView
from .views import IndexView
from django.conf.urls.static import static
from .views import ApplicationDeleteView
from django.urls import path
from .views import AllAppsListView, EditApp, AllCategoriesListView, EditCategory, CategoryDelete, CreateCategory, AllUsersListView, UserDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('success/', SuccessView.as_view(), name='success'),
    path('register/', RegisterView.as_view(), name='register'),  # Маршрут для регистрации
    path('login/', login_user, name='login'),  # URL для страницы входа
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # URL для выхода
    path('create_application/', CreateApplicationView.as_view(), name='create_application'),
    path('all-apps/', AllAppsListView.as_view(), name='all_apps'),
    path('all-categories/', AllCategoriesListView.as_view(), name='all_categories'),
    path('personal_account/', AccountListView.as_view(), name='personal_account'),
    path('application/delete_application/<int:pk>/', ApplicationDeleteView.as_view(), name='delete_application'),
    path('app/<int:pk>/edit/', EditApp.as_view(), name='app_edit'),
    path('category/<int:pk>/edit/', EditCategory.as_view(), name='edit_category'),
    path('category/delete/<int:pk>/', CategoryDelete.as_view(), name='delete_category'),
    path('category/create/', CreateCategory.as_view(), name='create_category'),
    path('all-users/', AllUsersListView.as_view(), name='all_users'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
