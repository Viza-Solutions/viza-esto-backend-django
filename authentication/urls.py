from django.urls import path
from .views import RegisterAPIView, LoginAPIView, AuthUserAPIView

from . import views


urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("user", AuthUserAPIView.as_view(), name="auth-user"),
    # path('verify-email/<uidb64>/<token>', VerifyEmail.as_view(), name='activate'),
    path("users/<int:pk>", views.user_detail),
    path("user_list", views.user_list),
]
