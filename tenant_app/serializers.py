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
