from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'learning_style', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('learning_style', 'interests', 'bio', 'avatar')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
