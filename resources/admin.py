from django.contrib import admin

from accounts.utils import log_action

from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "course", "year", "status", "uploaded_by")
    list_filter = ("type", "status")
    search_fields = ("title", "course", "uploaded_by__username")
    actions = ["approve_resources", "reject_resources"]

    @admin.action(description="Approve selected resources")
    def approve_resources(self, request, queryset):
        ids = list(queryset.values_list("id", flat=True))
        queryset.update(status=Resource.Status.APPROVED)
        for rid in ids:
            log_action(request.user, "approved", "resource", rid)

    @admin.action(description="Reject selected resources")
    def reject_resources(self, request, queryset):
        ids = list(queryset.values_list("id", flat=True))
        queryset.update(status=Resource.Status.REJECTED)
        for rid in ids:
            log_action(request.user, "rejected", "resource", rid)