

# Register your models here.
from django.contrib import admin
from django.utils import timezone

from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "is_featured", "published_at")
    list_filter = ("status", "is_featured")
    search_fields = ("title", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    actions = ["approve_blogs", "reject_blogs"]

    @admin.action(description="Approve selected blogs (publish)")
    def approve_blogs(self, request, queryset):
        queryset.update(
            status=Blog.Status.PUBLISHED,
            published_at=timezone.now(),
            reviewed_by=request.user,
            rejection_reason="",
        )

    @admin.action(description="Reject selected blogs")
    def reject_blogs(self, request, queryset):
        queryset.update(status=Blog.Status.REJECTED, reviewed_by=request.user)