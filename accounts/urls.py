from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import MeView, TeamListView

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    path("team/", TeamListView.as_view()),
]