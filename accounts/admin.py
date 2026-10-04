

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ActivityLog, Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active", "can_upload_resources")
    list_filter = ("role", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("WikiClub", {"fields": ("role", "can_upload_resources")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("WikiClub", {"fields": ("email", "role", "can_upload_resources")}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "member_title", "is_featured", "display_order")
    list_filter = ("member_title", "is_featured")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("actor", "action", "target_type", "created_at")