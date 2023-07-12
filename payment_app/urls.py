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
]
