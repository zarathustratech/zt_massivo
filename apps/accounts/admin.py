from django.contrib import admin
from apps.accounts.models import Account

from django.contrib.auth.admin import UserAdmin


@admin.register(Account)
class AccountAdmin(UserAdmin):
    ordering = ['id']
    list_display = (
        'id', 'first_name', 'last_name', 'company', 'email',
        'is_active', 'is_superuser',
    )
    list_filter = ('is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('password', )}),
        ('Contact', {'fields': ('first_name', 'last_name', 'company',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        ('Contact', {
            'fields': ('first_name', 'last_name', 'company'),
        }),
        ('Authentication', {
            'fields': ('email', 'password1', 'password2'),
        })
    )
