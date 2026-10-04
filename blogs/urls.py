from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MemberBlogViewSet, PublicBlogDetailView, PublicBlogListView

router = DefaultRouter()
router.register("member/blogs", MemberBlogViewSet, basename="member-blog")

urlpatterns = [
    path("blogs/", PublicBlogListView.as_view()),
    path("blogs/<slug:slug>/", PublicBlogDetailView.as_view()),
    path("", include(router.urls)),
]