from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Expense, ExpenseType  # Adjust the import paths as needed


@admin.register(ExpenseType)
class ExpenseTypeAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "parent")
    search_fields = ("name",)
    list_filter = ("parent",)


@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "amount",
        "description",
        "expense_type",
        "client",
        "linked_property",
        "added_by",
        "date",
    )
    search_fields = ("description", "expense_type__name", "client__name")
    list_filter = ("expense_type", "client", "linked_property", "added_by", "date")
