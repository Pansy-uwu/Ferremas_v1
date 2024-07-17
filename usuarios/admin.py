from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, AdminUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'rut', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'rut', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rut', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username', 'rut')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
