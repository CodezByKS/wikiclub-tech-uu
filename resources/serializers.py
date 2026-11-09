import os

from rest_framework import serializers

from accounts.serializers import display_name

from .models import Resource

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx", ".ppt", ".pptx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class PublicResourceSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = [
            "id", "title", "course", "year", "type",
            "file", "created_at", "uploaded_by_name",
        ]

    def get_uploaded_by_name(self, obj):
        return display_name(obj.uploaded_by)


class MemberResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            "id", "title", "course", "year", "type",
            "file", "status", "created_at",
        ]
        read_only_fields = ["status", "created_at"]

    def validate_file(self, f):
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                "Sirf PDF, image, Word ya PowerPoint file allowed hai."
            )
        if f.size > MAX_FILE_SIZE:
            raise serializers.ValidationError("File 10 MB se badi nahi honi chahiye.")
        return f