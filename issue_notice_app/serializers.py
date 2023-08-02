from rest_framework import serializers
from .models import *


class EstateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateIssue
        fields = "__all__"

        read_only_fields = ("added_by",)

    def create(self, validated_data):
        validated_data["added_by"] = self.context["request"].user
        return super().create(validated_data)


class TenantNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantNotice
        fields = "__all__"

        read_only_fields = ("posted_by",)

    def create(self, validated_data):
        validated_data["posted_by"] = self.context["request"].user
        return super().create(validated_data)
