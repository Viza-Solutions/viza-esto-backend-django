from django.db import models

from client_app.models import Client
from property_app.models import Property
from django.conf import settings
from tenant_app.models import *
from django.conf import settings


# Create your models here.
class EstateIssue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="estate_issues_added",
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="estate_issues_closed",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TenantNotice(models.Model):
    reason = models.TextField(null=True, blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    date_to_vacate = models.DateField()

    def __str__(self):
        return self.reason or "No reason provided"
