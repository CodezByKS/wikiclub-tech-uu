

# Create your models here.
from django.conf import settings
from django.db import models


class Resource(models.Model):
    class Type(models.TextChoices):
        PYQ = "PYQ", "PYQ"
        NOTES = "NOTES", "Notes"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    title = models.CharField(max_length=200)
    course = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PYQ)
    file = models.FileField(upload_to="resources/")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title