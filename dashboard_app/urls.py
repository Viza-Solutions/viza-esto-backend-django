from django.urls import path
from . import views

urlpatterns = [
    path("fetch_dashboard_data_client/<int:client_id>", views.fetch_dashboard_data_client, name="fetch_dashboard_data_client"),
    path("fetch_dashboard_data_property/<int:property_id>", views.fetch_dashboard_data_property, name="fetch_dashboard_data_property"),
    # Other URLs...
]
