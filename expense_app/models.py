from django.db import models

from client_app.models import *
from property_app.models import *
from django.conf import settings


class ExpenseType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    linked_property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    date = models.DateField()

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"
    

    
