from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from property_app.models import Room
from tenant_app.models import *
from payment_app.models import *
from .functions import *


@api_view(["POST"])
def sms_to_all_tenants(request, client_id):
    message = request.data.get("message")

    if not message:
        return Response(
            {"error": "Message not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    tenants = Tenant.objects.filter(deleted=False, client_id=client_id)

    for tenant in tenants:
        try:
            tenant_info(tenant, message)
        except Exception as e:
            print(f"Error processing tenant: {e}")

    return Response(
        {"message": "SMS sent to all property tenants"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def sms_to_property_tenants(request, property_id):
    message = request.data.get("message")

    if not message:
        return Response(
            {"error": "Message not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    tenants = Tenant.objects.filter(deleted=False, property_id=property_id).order_by(
        "fullname"
    )
    for tenant in tenants:
        try:
            tenant_info(tenant, message)
        except Exception as e:
            print(f"Error processing tenant: {e}")

    return Response(
        {"message": "SMS sent to all property tenants"}, status=status.HTTP_200_OK
    )


def tenant_info(tenant, message):
    fullname = tenant.fullname
    email = tenant.email
    phone_number = tenant.phone_number
    client_id = tenant.client_id

    try:
        send_sms(message, [phone_number], client_id)
    except Exception as e:
        print(f"Error sending SMS to tenant {fullname}: {e}")
