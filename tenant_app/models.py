from django.db import models
from django.core.exceptions import ValidationError
from client_app.models import Client
from property_app.models import Property, Room
from django.conf import settings


class Tenant(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    fullname = models.CharField(max_length=255)
    alternative_names = models.TextField(blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    deposit_amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fullname}"

    def save(self, *args, **kwargs):
        # Convert the name and alternative names to title case before saving
        self.fullname = self.fullname.title()
        self.alternative_names = self.alternative_names.title()
        super(Tenant, self).save(*args, **kwargs)
