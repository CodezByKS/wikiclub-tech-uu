from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Blog
from .serializers import MemberBlogSerializer, PublicBlogSerializer, unique_slug


class PublicBlogListView(generics.ListAPIView):
    """Sirf PUBLISHED blogs. ?featured=true se sirf featured."""
    serializer_class = PublicBlogSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            Blog.objects.filter(status=Blog.Status.PUBLISHED)
            .select_related("author", "author__profile")
            .order_by("-published_at")
        )
        if self.request.query_params.get("featured") == "true":
            qs = qs.filter(is_featured=True)
        return qs


class PublicBlogDetailView(generics.RetrieveAPIView):
    serializer_class = PublicBlogSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Blog.objects.filter(status=Blog.Status.PUBLISHED).select_related(
            "author", "author__profile"
        )


class MemberBlogViewSet(viewsets.ModelViewSet):
    """Member sirf apne blogs dekh/edit/delete kar sakta hai."""
    serializer_class = MemberBlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user).order_by("-updated_at")

    def _ensure_editable(self, blog):
        if blog.status not in (Blog.Status.DRAFT, Blog.Status.REJECTED):
            raise PermissionDenied(
                "Sirf Draft ya Rejected blog edit ho sakta hai. "
                "Pending ya Published blog me badlav nahi ho sakta."
            )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            slug=unique_slug(serializer.validated_data["title"]),
            status=Blog.Status.DRAFT,
        )

    def perform_update(self, serializer):
        self._ensure_editable(serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_editable(instance)
        instance.delete()

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Blog ko admin review ke liye bhejna (DRAFT/REJECTED -> PENDING)."""
        blog = self.get_object()
        self._ensure_editable(blog)
        blog.status = Blog.Status.PENDING
        blog.rejection_reason = ""
        blog.save(update_fields=["status", "rejection_reason", "updated_at"])
        return Response(MemberBlogSerializer(blog, context={"request": request}).data)