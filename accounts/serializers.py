from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile, User


def display_name(user):
    return user.get_full_name() or user.username


class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    """Login me username ki jagah email bhi chalega."""

    def validate(self, attrs):
        identifier = attrs.get("username", "")
        if "@" in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
            if user:
                attrs["username"] = user.username
        return super().validate(attrs)


class MyProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    name = serializers.SerializerMethodField()
    can_upload_resources = serializers.BooleanField(source="user.can_upload_resources", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id", "username", "name", "email", "role",
            "photo", "member_title", "role_label", "public_email",
            "bio", "github", "linkedin", "is_featured", "show_on_team", "can_upload_resources",
        ]
        # member ye fields khud nahi badal sakta, sirf admin badlega
        read_only_fields = ["member_title", "role_label", "is_featured", "show_on_team"]

    def get_name(self, obj):
        return display_name(obj.user)


class TeamMemberSerializer(serializers.ModelSerializer):
    """Output frontend ke TeamMember type jaisa hai."""
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    roleType = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    email = serializers.CharField(source="public_email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "name", "role", "roleType", "image", "email", "linkedin", "github", "bio"]

    def get_name(self, obj):
        return display_name(obj.user)

    def get_role(self, obj):
        return obj.role_label or obj.get_member_title_display()

    def get_roleType(self, obj):
        return obj.member_title.lower()

    def get_image(self, obj):
        if not obj.photo:
            return ""
        request = self.context.get("request")
        url = obj.photo.url
        return request.build_absolute_uri(url) if request else url