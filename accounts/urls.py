from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, MeView, TeamListView

urlpatterns = [
    path("auth/login/", LoginView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    path("team/", TeamListView.as_view()),
]