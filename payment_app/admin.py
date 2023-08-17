from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    PaymentMethod,
    PaymentTransaction,
)  # Adjust the import paths as needed


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "client",
        "added_by",
        "deleted",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "client__name", "added_by__username")
    list_filter = ("client", "deleted", "created_at", "updated_at")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "tenant",
        "amount",
        "balance",
        "month",
        "year",
        "payment_method",
        "reference",
        "processed_by",
        "client",
        "reversed",
        "uuid",
        "date_of_payment",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "tenant__name",
        "reference",
        "payment_method__name",
        "client__name",
    )
    list_filter = (
        "month",
        "year",
        "payment_method",
        "processed_by",
        "client",
        "reversed",
        "date_of_payment",
        "created_at",
        "updated_at",
    )
