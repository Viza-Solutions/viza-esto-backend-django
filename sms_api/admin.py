from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import SmsCredential  # Adjust the import paths as needed


@admin.register(SmsCredential)
class SmsCredentialAdmin(ImportExportModelAdmin):
    list_display = ("id", "client", "username")
    search_fields = ("client__name", "username")
    list_filter = ("client",)
