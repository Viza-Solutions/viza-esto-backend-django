from django.urls import path
from .views import *

from . import views


urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("user", AuthUserAPIView.as_view(), name="auth-user"),
    # path('verify-email/<uidb64>/<token>', VerifyEmail.as_view(), name='activate'),
    path("users/<int:pk>", views.user_detail),
    path("user_list/<int:client_id>", views.user_list),
    path("users/update/<int:pk>", user_update, name="user-partial-update"),
    # user_mapping
    path("prop-assign/get_all", get_user_mappings_all, name="get_user_mappings_all"),
    path("prop-assign/get/<int:user_id>", get_user_mappings, name="get_user_mappings"),
    path("prop-assign", create_user_mapping, name="create_user_mapping"),
    path("prop-assign/del/<int:pk>", delete_user_mapping, name="delete_user_mapping"),
]
