from django.contrib import admin
from django.utils import timezone

from accounts.utils import log_action

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
        ids = list(queryset.values_list("id", flat=True))
        queryset.update(
            status=Blog.Status.PUBLISHED,
            published_at=timezone.now(),
            reviewed_by=request.user,
            rejection_reason="",
        )
        for bid in ids:
            log_action(request.user, "approved", "blog", bid)

    @admin.action(description="Reject selected blogs")
    def reject_blogs(self, request, queryset):
        ids = list(queryset.values_list("id", flat=True))
        queryset.update(status=Blog.Status.REJECTED, reviewed_by=request.user)
        for bid in ids:
            log_action(request.user, "rejected", "blog", bid)