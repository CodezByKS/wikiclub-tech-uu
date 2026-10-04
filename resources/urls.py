from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MemberResourceViewSet, PublicResourceListView

router = DefaultRouter()
router.register("member/resources", MemberResourceViewSet, basename="member-resource")

urlpatterns = [
    path("resources/", PublicResourceListView.as_view()),
    path("", include(router.urls)),
]