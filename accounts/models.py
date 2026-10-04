

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    can_upload_resources = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)


class Profile(models.Model):
    class Title(models.TextChoices):
        COORDINATOR = "COORDINATOR", "Project Coordinator"
        MENTOR = "MENTOR", "Mentor"
        ENVOY = "ENVOY", "Campus Envoy"
        LEAD = "LEAD", "Team Lead"
        VOLUNTEER = "VOLUNTEER", "Volunteer"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    member_title = models.CharField(max_length=20, choices=Title.choices, default=Title.VOLUNTEER)
    role_label = models.CharField(max_length=100, blank=True)  # jaise "ML-Lead"
    public_email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    show_on_team = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class ActivityLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} - {self.action}"