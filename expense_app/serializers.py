from rest_framework import serializers
from .models import Expense, ExpenseType

class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    # expense_type = ExpenseTypeSerializer()

    class Meta:
        model = Expense
        fields = '__all__'
