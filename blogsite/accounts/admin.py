from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    """
    custom user admin pannel
    """
    model = User
    list_display = (
    "email",
    "is_staff",
    "is_superuser",
    "is_active",
    "updated_at",)
    list_filter = ["is_superuser", "updated_at", "created_at"]
    search_fields = ['email']
    ordering = ("-updated_at", "-created_at")
    readonly_fields = (
    "created_at",
    "updated_at",
    "last_login",)
    # it visualize our admin user pannel
    fieldsets = (
        ("Authentication", {
            "fields": ("email", "password"),
        }),
        ("Permissions", {
            "fields": (
                "is_staff", "is_superuser", "is_active"
            ),
        }),
        ("Group Permissins", {
            "fields": ("groups", "user_permissions"),
        }),
        ("Dates", {
            "fields": ("last_login","created_at", "updated_at",),
        }),
    )
    # it visualize our admin add user pannel
    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            "fields": ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')
        }),
    )
    
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)