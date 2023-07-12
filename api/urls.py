from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("client/", include("client_app.urls")),
    path("property/", include("property_app.urls")),
    path("tenant/", include("tenant_app.urls")),
]
