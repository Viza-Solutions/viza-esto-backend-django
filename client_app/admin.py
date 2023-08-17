from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Client  # Adjust the import path as needed


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "address",
        "country",
        "city",
        "zip_code",
        "status",
        "email",
        "deleted",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "phone_number", "email")
    list_filter = ("status", "deleted")


