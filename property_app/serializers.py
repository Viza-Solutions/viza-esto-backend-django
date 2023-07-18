from rest_framework import serializers
from .models import *


# class PropertySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Property
#         fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

    def to_internal_value(self, data):
        # Convert the 'name' field to title case
        data["name"] = data.get("name", "").title()
        return super().to_internal_value(data)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"
