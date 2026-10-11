from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile
from .serializers import (
    EmailOrUsernameTokenSerializer,
    MyProfileSerializer,
    TeamMemberSerializer,
)


class LoginView(TokenObtainPairView):
    """Username ya email, dono se login."""
    serializer_class = EmailOrUsernameTokenSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """Logged-in member ka apna profile: dekhna aur edit karna."""
    serializer_class = MyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class TeamListView(generics.ListAPIView):
    """Public team list. ?featured=true se sirf featured members."""
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            Profile.objects.filter(user__is_active=True, show_on_team=True)
            .select_related("user")
            .order_by("display_order", "id")
        )
        if self.request.query_params.get("featured") == "true":
            qs = qs.filter(is_featured=True)
        return qs