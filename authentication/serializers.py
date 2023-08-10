from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "user_status",
            "user_type",
            "last_name",
            "phone_number",
            "first_name",
            "token",
            "client",
            "propertyy",
        ]
        read_only_fields = [
            "id",
            "user_status",
            "user_type",
            "last_name",
            "phone_number",
            "first_name",
            "token",
            "username",
            "client",
            "propertyy",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "is_active",
        )


class UserSerializerrrrr(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_status",
            "user_type",
            "propertyy",
            "client",
            "created_at",
            "updated_at",
        ]


class UserMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMapping
        fields = "__all__"


from property_app.models import *

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

class UserMappingSerializer(serializers.ModelSerializer):
    property_linked = PropertySerializer()
    
    class Meta:
        model = UserMapping
        fields = "__all__"