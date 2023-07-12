from django.urls import path
from tenant_app import views

urlpatterns = [
    path("tenants", views.tenant_list, name="tenant-list"),
    path("tenants/<int:pk>", views.retrieve_tenant, name="retrieve-tenant"),
    path("tenants/create", views.create_tenant, name="create-tenant"),
    path("tenants/update/<int:pk>", views.update_tenant, name="update-tenant"),
    path("tenants/delete/<int:pk>", views.delete_tenant, name="delete-tenant"),
    path("tenants/delete-all", views.delete_all_tenants, name="delete-all-tenants"),
    path(
        "clients/tenants/<int:client_id>",
        views.client_tenant_list,
        name="client_tenant_list",
    ),
    path(
        "properties/tenants/<int:property_id>",
        views.property_tenant_list,
        name="property_tenant_list",
    ),
    path(
        "tenants/transfer-room/<int:pk>",
        views.transfer_tenant_room,
        name="transfer_tenant_room",
    ),
]
