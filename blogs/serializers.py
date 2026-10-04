from django.utils.text import slugify
from rest_framework import serializers

from accounts.serializers import display_name

from .models import Blog


def unique_slug(title):
    base = slugify(title) or "post"
    slug, n = base, 2
    while Blog.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


class PublicBlogSerializer(serializers.ModelSerializer):
    """Website pe dikhne wala blog, author ke naam aur profile ke saath."""
    author_name = serializers.SerializerMethodField()
    author_title = serializers.SerializerMethodField()
    author_photo = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id", "title", "slug", "content", "cover_image",
            "is_featured", "published_at",
            "author_name", "author_title", "author_photo",
        ]

    def get_author_name(self, obj):
        return display_name(obj.author)

    def get_author_title(self, obj):
        profile = getattr(obj.author, "profile", None)
        return profile.get_member_title_display() if profile else ""

    def get_author_photo(self, obj):
        profile = getattr(obj.author, "profile", None)
        if profile and profile.photo:
            request = self.context.get("request")
            url = profile.photo.url
            return request.build_absolute_uri(url) if request else url
        return None


class MemberBlogSerializer(serializers.ModelSerializer):
    """Member ke apne blog ke liye. Status/slug member khud nahi badal sakta."""

    class Meta:
        model = Blog
        fields = [
            "id", "title", "slug", "content", "cover_image",
            "status", "rejection_reason", "is_featured",
            "published_at", "created_at", "updated_at",
        ]
        read_only_fields = [
            "slug", "status", "rejection_reason", "is_featured",
            "published_at", "created_at", "updated_at",
        ]