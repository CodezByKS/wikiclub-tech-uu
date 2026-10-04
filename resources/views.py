from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Resource
from .serializers import MemberResourceSerializer, PublicResourceSerializer


class PublicResourceListView(generics.ListAPIView):
    """Sirf APPROVED resources. Filters: ?type=PYQ&course=DBMS&year=2024"""
    serializer_class = PublicResourceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            Resource.objects.filter(status=Resource.Status.APPROVED)
            .select_related("uploaded_by")
            .order_by("-year", "-created_at")
        )
        params = self.request.query_params
        if params.get("type"):
            qs = qs.filter(type=params["type"].upper())
        if params.get("course"):
            qs = qs.filter(course__icontains=params["course"])
        if params.get("year"):
            qs = qs.filter(year=params["year"])
        return qs


class MemberResourceViewSet(viewsets.ModelViewSet):
    """Member sirf apne uploads dekh/edit/delete kar sakta hai."""
    serializer_class = MemberResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resource.objects.filter(uploaded_by=self.request.user).order_by("-created_at")

    def _ensure_editable(self, resource):
        if resource.status == Resource.Status.APPROVED:
            raise PermissionDenied("Approved resource me badlav nahi ho sakta.")

    def perform_create(self, serializer):
        user = self.request.user
        if not (user.can_upload_resources or user.role == "ADMIN"):
            raise PermissionDenied("Aapko resources upload karne ki permission nahi hai.")
        serializer.save(uploaded_by=user, status=Resource.Status.PENDING)

    def perform_update(self, serializer):
        self._ensure_editable(serializer.instance)
        # edit ke baad dobara review ke liye wapas Pending
        serializer.save(status=Resource.Status.PENDING)

    def perform_destroy(self, instance):
        self._ensure_editable(instance)
        instance.delete()