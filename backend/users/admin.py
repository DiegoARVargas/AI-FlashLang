from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_premium", "preferred_language", "is_staff", "display_name")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_premium", "preferred_language", "display_name", "avatar")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)