from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import EstateIssue, TenantNotice  # Adjust the import paths as needed


@admin.register(EstateIssue)
class EstateIssueAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "title",
        "client",
        "added_by",
        "property",
        "is_open",
        "closed_by",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "client__name", "added_by__username", "property__name")
    list_filter = ("is_open", "created_at", "updated_at")


@admin.register(TenantNotice)
class TenantNoticeAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "tenant",
        "client",
        "posted_by",
        "property",
        "date_to_vacate",
        "is_active",
    )
    search_fields = (
        "tenant__name",
        "client__name",
        "posted_by__username",
        "property__name",
    )
    list_filter = ("is_active", "date_to_vacate")
