from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Tenant  # Adjust the import paths as needed


@admin.register(Tenant)
class TenantAdmin(ImportExportModelAdmin):
    list_display = (
        "fullname",
        "alternative_names",
        "id_number",
        "email",
        "phone_number",
        "date_of_birth",
        "date_of_lease",
        "gender",
        "client",
        "added_by",
        "property",
        "room",
        "status",
        "deposit_amount_paid",
        "date_of_deposit",
        "deleted",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "fullname",
        "alternative_names",
        "id_number",
        "email",
        "phone_number",
        "client__name",
        "property__name",
        "room__room_number",
    )
    list_filter = (
        "gender",
        "client",
        "property",
        "room",
        "status",
        "deleted",
        "created_at",
        "updated_at",
    )

