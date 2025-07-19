from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "username", "is_active", "is_staff", "is_superuser", "is_premium", "preferred_language")
    list_filter = ("is_active", "is_staff", "is_superuser", "is_premium", "preferred_language")
    search_fields = ("email", "username", "display_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("username", "display_name", "avatar", "preferred_language")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "is_premium", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "username", "preferred_language", "is_premium", "is_staff", "is_superuser"),
        }),
    )