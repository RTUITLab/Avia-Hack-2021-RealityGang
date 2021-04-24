from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import *

AdminSite.index_title = 'Администрирование проекта'
AdminSite.site_title = 'Avia-Hack-2021'
AdminSite.site_header = 'Avia-Hack-2021'


class CustomMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'user', 'description')


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Авторизация', {'fields': ('username', 'password')}),
        ('Основная информация', {'fields': ('full_name',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Другое', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Авторизация', {'fields': ('username', 'password1', 'password2',)}),
        ('Основная информация', {'fields': ('full_name',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Message, CustomMessageAdmin)
