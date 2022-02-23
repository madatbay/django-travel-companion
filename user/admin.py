from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "avatar_preview",
    )

    fieldsets = (
        (None, {"fields": ("email", "full_name", "password")}),
        (
            "Personal info",
            {"fields": ("avatar",)},
        ),
        ("Important dates", {"fields": ("created_at",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "full_name",
                    "avatar",
                ),
            },
        ),
    )
    ordering = ("email",)
    search_fields = ("email",)
    readonly_fields = ("created_at",)
