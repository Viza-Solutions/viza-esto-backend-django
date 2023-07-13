from rest_framework import serializers
from .models import *


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


# class PaymentMethodUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentMethod
#         exclude = ["client", "added_by"]


# class PaymentTransactionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = PaymentTransaction
#         exclude = ["balance", "month", "year"]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    year = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = PaymentTransaction
        exclude = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['balance'] = instance.balance
        representation['month'] = instance.month
        representation['year'] = instance.year
        representation['uuid'] = instance.uuid
        return representation