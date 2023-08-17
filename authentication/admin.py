from django.contrib import admin
from .models import User
from import_export.admin import ImportExportModelAdmin


# admin.site.register(User)
@admin.register(User)
class User(ImportExportModelAdmin):
    list_display = ("id", "email")
