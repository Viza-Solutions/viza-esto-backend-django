from django.db import models

# from django.contrib.auth.models import User
from client_app.models import *
from django.conf import settings


from django.db import models
from django.conf import settings


class Property(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    name = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    country = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    rooms = models.PositiveIntegerField(default=30)
    deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Convert the name to title case before saving
        self.name = self.name.title()
        super(Property, self).save(*args, **kwargs)


class RoomType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ("bedsitter", "Bedsitter"),
        ("one_bedroom", "One Bedroom"),
        ("two_bedroom", "Two Bedroom"),
        ("studio", "Studio Apartment"),
        ("penthouse", "Penthouse"),
        ("duplex", "Duplex"),
        ("loft", "Loft"),
        ("efficiency", "Efficiency Apartment"),
        ("shared", "Shared Room"),
        ("suite", "Suite"),
        ("meeting", "Meeting Room"),
        ("conference", "Conference Room"),
        ("office", "Office Space"),
        ("retail", "Retail Space"),
        ("others", "Others"),
        # Add more choices as needed
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=50, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    size = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["property", "room_number"]

    def __str__(self):
        return f"{self.room_number} ({self.property.name})"
