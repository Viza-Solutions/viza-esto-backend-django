from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns...
    path("payment-methods", payment_method_list, name="payment_method_list"),
    path(
        "clients/payment-methods/<int:client_id>",
        client_payment_method_list,
        name="client_payment_method_list",
    ),
    path(
        "payment-methods/create",
        create_payment_method,
        name="create_payment_method",
    ),
    path(
        "payment-methods/<int:pk>",
        retrieve_payment_method,
        name="retrieve_payment_method",
    ),
    path(
        "payment-methods/update/<int:pk>",
        update_payment_method,
        name="update_payment_method",
    ),
    path(
        "payment-methods/delete/<int:pk>",
        delete_payment_method,
        name="delete_payment_method",
    ),
    path(
        "payment-transactions",
        create_payment_transaction,
        name="create_payment_transaction",
    ),
    path(
        "payment-transactions/delete-all",
        delete_all_payment_transactions,
        name="delete-all-payment-transactions",
    ),
    # reports
    path("excel-report/<int:tenant_id>", excel_report_view, name="excel_report"),
    path('pdf_report/<int:tenant_id>', pdf_report_view, name='pdf_report_view'),



    # get trasactions
    path('tenant-transactions/<int:tenant_id>', get_transactions_for_tenant, name='get_transactions_for_tenant'),


]
