from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'phone', 'username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'username', 'email')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('个人信息', {'fields': ('username', 'email', 'address', 'avatar')}),
        ('权限信息', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    ordering = ('id',)

admin.site.register(User, UserAdmin)
