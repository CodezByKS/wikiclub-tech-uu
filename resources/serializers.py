from rest_framework import serializers

from accounts.serializers import display_name

from .models import Resource


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