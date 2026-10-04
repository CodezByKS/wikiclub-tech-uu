from django.contrib import admin

# Register your models here.


from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "course", "year", "status", "uploaded_by")
    list_filter = ("type", "status")