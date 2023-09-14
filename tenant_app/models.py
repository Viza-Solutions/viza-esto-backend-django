from django.db import models
from client_app.models import Client
from property_app.models import Property, Room
from django.conf import settings
from django.core.validators import RegexValidator


class KenyanPhoneNumberField(models.CharField):
    default_validators = [
        RegexValidator(
            regex=r"^\+254\d{9}$",
            message="Phone number must be in the format +254XXXXXXXXX.",
            code="invalid_phone_number",
        )
    ]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 13  # "+254" plus 9 digits
        super().__init__(*args, **kwargs)


class Tenant(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    INTRO_CHOICES = [
        ("Self", "Self"),
        ("Agent", "Agent"),
    ]
    fullname = models.CharField(max_length=255)
    alternative_names = models.CharField(blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # phone_number = KenyanPhoneNumberField()
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)

    date_of_lease = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
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
    date_of_deposit = models.DateTimeField(blank=True, null=True)

    deleted = models.BooleanField(default=False)

    # next of kin
    next_of_kin = models.CharField(blank=True, null=True)
    next_of_kin_contact = models.CharField(blank=True, null=True)

    # AGENT
    intro_by = models.CharField(
        max_length=5,  # Adjust the max_length according to your needs
        choices=INTRO_CHOICES,
        default="Self",
    )
    agent_name = models.CharField(max_length=50, blank=True, null=True)
    agent_phone = KenyanPhoneNumberField(blank=True, null=True)
    agent_id_number = models.CharField(max_length=50, blank=True, null=True)
    agent_commission = models.CharField(max_length=50, blank=True, null=True)
    agent_trasaction_ref = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fullname}"

    def save(self, *args, **kwargs):
        # Convert the name and alternative names to title case before saving
        self.fullname = self.fullname.title()
        self.alternative_names = self.alternative_names.title()
        super(Tenant, self).save(*args, **kwargs)
