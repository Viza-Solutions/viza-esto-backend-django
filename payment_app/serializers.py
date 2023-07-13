from rest_framework import serializers
from .models import *
from uuid import UUID


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class PaymentMethodUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        exclude = ["client", "added_by"]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    year = serializers.ReadOnlyField()
    uuid = serializers.CharField(read_only=True)

    class Meta:
        model = PaymentTransaction
        exclude = []
