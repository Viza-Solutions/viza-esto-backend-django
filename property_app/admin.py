from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Property, RoomType, Room  # Adjust the import paths as needed


@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "client",
        "added_by",
        "country",
        "town",
        "address",
        "deleted",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "client__name", "country", "town", "address")
    list_filter = ("client", "deleted", "status", "created_at", "updated_at")


@admin.register(RoomType)
class RoomTypeAdmin(ImportExportModelAdmin):
    list_display = ("name", "description", "added_by")
    search_fields = ("name",)
    list_filter = ()


@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    list_display = (
        "room_number",
        "property",
        "floor",
        "is_available",
        "room_type",
        "client",
        "added_by",
        "deleted",
        "created_at",
        "updated_at",
    )
    search_fields = ("room_number", "property__name", "client__name")
    list_filter = ("property", "room_type", "client", "is_available", "deleted")

