from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"

        def to_internal_value(self, data):
            # Convert the 'name' field to title case
            data["fullname"] = data.get("fullname", "").title()
            data["alternative_names"] = data.get("alternative_names", "").title()
            return super().to_internal_value(data)


class TenantRoomTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["room"]


class TenantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "fullname",
            "alternative_names",
            "id_number",
            "email",
            "phone_number",
            "deposit_amount_paid",
            "status",
        ]

        def save(self, *args, **kwargs):
            # Convert the name and alternative names to title case before saving
            self.fullname = self.fullname.title()
            self.alternative_names = self.alternative_names.title()
            super().save(*args, **kwargs)
