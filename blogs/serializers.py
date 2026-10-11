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
    """Website pe dikhne wala blog. Keys frontend ke hisaab se rakhi hain."""
    image = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source="published_at", read_only=True)
    author = serializers.SerializerMethodField()
    author_title = serializers.SerializerMethodField()
    author_photo = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id", "title", "slug", "content", "excerpt", "tags", "is_featured",
            "image", "date", "author", "author_title", "author_photo",
        ]

    def _absolute(self, url):
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request else url

    def get_image(self, obj):
        if obj.cover_image:
            return self._absolute(obj.cover_image.url)
        return obj.cover_image_url or ""

    def get_author(self, obj):
        return display_name(obj.author)

    def get_author_title(self, obj):
        profile = getattr(obj.author, "profile", None)
        return (profile.role_label or profile.get_member_title_display()) if profile else ""

    def get_author_photo(self, obj):
        profile = getattr(obj.author, "profile", None)
        if profile and profile.photo:
            return self._absolute(profile.photo.url)
        return None


class MemberBlogSerializer(serializers.ModelSerializer):
    """Member ke apne blog ke liye. Status/slug member khud nahi badal sakta."""

    class Meta:
        model = Blog
        fields = [
            "id", "title", "slug", "excerpt", "tags", "content", "cover_image",
            "status", "rejection_reason", "is_featured",
            "published_at", "created_at", "updated_at",
        ]
        read_only_fields = [
            "slug", "status", "rejection_reason", "is_featured",
            "published_at", "created_at", "updated_at",
        ]