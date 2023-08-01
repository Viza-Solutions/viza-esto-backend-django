from rest_framework import serializers
from .models import *


class EstateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateIssue
        fields = "__all__"


class TenantNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantNotice
        fields = "__all__"
