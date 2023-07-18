from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"


class TenantRoomTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["room"]

        def to_internal_value(self, data):
            # Convert the 'name' field to title case
            data["fullname"] = data.get("fullname", "").title()
            return super().to_internal_value(data)


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

        def to_internal_value(self, data):
            # Convert the 'name' field to title case
            data["fullname"] = data.get("fullname", "").title()
            return super().to_internal_value(data)

