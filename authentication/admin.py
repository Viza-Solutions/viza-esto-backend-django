from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *  # Adjust the import path as needed


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
        "is_verified",
        "first_name",
        "last_name",
        "phone_number",
        "user_type",
        "user_status",
        "propertyy",
        "client",
        "created_at",
        "updated_at",
    )
    search_fields = ("email", "username", "phone_number")
    list_filter = ["client"]


@admin.register(UserMapping)
class UserMappingAdmin(admin.ModelAdmin):
    list_display = ("user", "property_linked")
    search_fields = (
        "user__email",
        "user__username",
        "property_linked__name",
    )  # Adjust the fields accordingly
    list_filter = ("user", "property_linked")
