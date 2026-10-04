from rest_framework import serializers

from .models import Profile


def display_name(user):
    return user.get_full_name() or user.username


class MyProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id", "username", "name", "email", "role",
            "photo", "member_title", "bio", "github", "linkedin", "is_featured",
        ]
        # member ye fields khud nahi badal sakta, sirf admin badlega
        read_only_fields = ["member_title", "is_featured"]

    def get_name(self, obj):
        return display_name(obj.user)


class TeamMemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id", "name", "photo", "member_title",
            "bio", "github", "linkedin", "is_featured",
        ]

    def get_name(self, obj):
        return display_name(obj.user)