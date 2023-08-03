from django.db import models
from django.contrib.auth.models import User
from client_app.models import *
from tenant_app.models import *
from django.conf import settings
from uuid import uuid4


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("name", "client"),)

    def __str__(self):
        return self.name


class PaymentTransaction(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255)
    description = models.TextField()
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reversed = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    date_of_payment = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PaymentTransaction - ID: {self.id}"
