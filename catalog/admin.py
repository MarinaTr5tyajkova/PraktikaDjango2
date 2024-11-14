from django.contrib import admin
from .models import Category, Application

class ApplicationAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated  # Проверяем, авторизован ли пользователь

# Register your models here.
admin.site.register(Category)
admin.site.register(Application, ApplicationAdmin)