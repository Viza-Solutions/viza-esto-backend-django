from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tenant
from property_app.models import Property, Room
from payment_app.models import *
from .serializers import *
from rest_framework import serializers

from datetime import datetime
 

@api_view(["GET"])
def tenant_list(request):
    tenants = Tenant.objects.filter(deleted=False).order_by("fullname")
    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data)


# Get all tenants for a specific client
@api_view(["GET"])
def client_tenant_list(request, client_id):
    tenants = Tenant.objects.filter(deleted=False, client_id=client_id).order_by(
        "fullname"
    )
    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data)


# Get all tenants for a specific property
@api_view(["GET"])
def property_tenant_list(request, property_id):
    tenants = Tenant.objects.filter(deleted=False, property_id=property_id).order_by(
        "fullname"
    )
    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_tenant(request):
    serializer = TenantSerializer(data=request.data)
    if serializer.is_valid():
        tenant = serializer.validated_data

        # property_id = request.data.get("property")
        room = tenant.get("room")
        property_id = tenant.get("property").id

        try:
            property_ = Property.objects.get(id=property_id)
            if room.property_id != property_id:
                raise serializers.ValidationError(
                    {
                        "error": "The provided room does not belong to the specified property."
                    }
                )
        except Property.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "Invalid property_id provided."}
            )

        # Check if the user with the same fullname already exists in the same property
        title_case_name = tenant["fullname"].title()
        existing_tenants = Tenant.objects.filter(
            fullname=title_case_name, property=tenant["property"], deleted=False
        )
        if "id" in tenant:
            # Exclude the current instance when checking for duplicates during update
            existing_tenants = existing_tenants.exclude(pk=tenant["id"])

        if existing_tenants.exists():
            raise serializers.ValidationError(
                {
                    "error": f"A tenant with the name '{title_case_name}' already exists in the property."
                }
            )

        # Check if the room is available
        if not room.is_available:
            raise serializers.ValidationError(
                {"error": "The selected room is not available for allocation."}
            )

        # Check if the room is deleted
        if room.deleted:
            raise serializers.ValidationError(
                {"error": "The selected room has been deleted."}
            )

        added_by = request.user

        tenant_instance = Tenant(
            fullname=tenant["fullname"],
            alternative_names=tenant.get("alternative_names"),
            id_number=tenant.get("id_number"),
            email=tenant.get("email"),
            phone_number=tenant["phone_number"],
            client=tenant["client"],
            added_by=added_by,
            deleted=False,
            property=tenant["property"],
            room=room,
            status=tenant["status"],
            deposit_amount_paid=tenant.get("deposit_amount_paid"),
        )

        tenant_instance.save()

        # Update the room's is_available field to False
        room.is_available = False
        room.save()

        serializer = TenantSerializer(tenant_instance)

        return Response(
            {"message": "Tenant created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_tenant(request, pk):
    try:
        tenant = Tenant.objects.get(pk=pk, deleted=False)
        serializer = TenantSerializer(tenant)

        current_datetime = datetime.now()

        # Get the current month and year
        current_month = int(current_datetime.month)
        current_year = int(current_datetime.year)

        try:
            queryset = PaymentTransaction.objects.filter(tenant_id=pk, reversed=False)
            # Calculate unpaid and prepaid months
            last_transaction = queryset.order_by("-id").first()
            balance = int(last_transaction.balance)
            year = int(last_transaction.year)
            month = int(last_transaction.month)

            try:
                tenant_details = Tenant.objects.get(pk=pk)
                room_id = tenant_details.room_id
                name = (
                    tenant_details.fullname
                )  # Set the 'name' variable with the tenant's name

                # Get the room object using the retrieved room_id
                room = Room.objects.get(pk=room_id)
                room_number = room.room_number
                estate = str(room.property)
                monthly_price = int(room.monthly_price)

            except Tenant.DoesNotExist:
                # Handle the case when no tenant is found for the given tenant_id
                room_id = None
                monthly_price = None
                name = "Undefined"

            # Calculate the curr_balance
            months_difference = ((current_year - year) * 12) + (current_month - month)

            curr_balance = (-months_difference * monthly_price) + balance

            if curr_balance > 0:
                curr_balance_str = "Prepaid Amount Ksh. " + str(curr_balance) + "/="
                typee = "Prepaid"
            elif curr_balance == 0:
                # curr_balance_str = str(curr_balance) + ""
                curr_balance_str =  "All Rent balance has been cleared"
                typee = "Cleared"
            else:
                curr_balance_str = "Balance of Amount Ksh. " + str(curr_balance) + "/="
                typee = "Balance"
        except:
            typee = "N/A"
            curr_balance = "N/A"
            curr_balance_str = "No payment has ever been done"

        return Response(
            {
                "data": serializer.data,
                "type": typee,
                "amount": curr_balance,
                "full_resp": curr_balance_str,
            }
        )
    except Tenant.DoesNotExist:
        return Response(
            {"message": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
def update_tenant(request, pk):
    try:
        tenant = Tenant.objects.get(pk=pk, deleted=False)
        serializer = TenantUpdateSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            updated_tenant = serializer.validated_data

            title_case_name = updated_tenant.get("fullname").title()

            existing_tenants = Tenant.objects.filter(
                fullname=title_case_name,
                property=tenant.property,
                deleted=False,
            ).exclude(pk=pk)

            if existing_tenants.exists():
                raise serializers.ValidationError(
                    {
                        "error": f"A tenant with the name '{title_case_name}' already exists in the property."
                    }
                )

            # Update the tenant instance
            serializer.save()

            return Response(
                {"message": "Tenant updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Tenant.DoesNotExist:
        return Response(
            {"message": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
def transfer_tenant_room(request, pk):
    try:
        tenant = Tenant.objects.get(pk=pk, deleted=False)
        serializer = TenantRoomTransferSerializer(
            tenant, data=request.data, partial=True
        )
        if serializer.is_valid():
            updated_tenant = serializer.validated_data

            new_room = updated_tenant.get("room")
            property_id = tenant.property.id

            if new_room.property.id != property_id:
                raise serializers.ValidationError(
                    {
                        "error": "You can only transfer the tenant within the same property."
                    }
                )

            if not new_room.is_available:
                raise serializers.ValidationError(
                    {"error": "The selected room is not available for allocation."}
                )

            if new_room.deleted:
                raise serializers.ValidationError(
                    {"error": "The selected room has been deleted."}
                )

            old_room = tenant.room

            # Update the tenant's room
            tenant.room = new_room
            tenant.save()

            # Set is_available field of the old and new rooms
            old_room.is_available = True
            old_room.save()

            new_room.is_available = False
            new_room.save()

            return Response(
                {"message": "Tenant room transfer successful", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Tenant.DoesNotExist:
        return Response(
            {"message": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
def delete_tenant(request, pk):
    try:
        tenant = Tenant.objects.get(pk=pk, deleted=False)
        room_id = tenant.room.id  # Get the room ID from the tenant object
        tenant.deleted = True
        tenant.save()

        # Update the room's is_available field to True
        room = Room.objects.get(pk=room_id)  # Assuming you have a Room model
        room.is_available = True
        room.save()

        return Response(
            {"message": "Tenant deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Tenant.DoesNotExist:
        return Response(
            {"message": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND
        )


# delete-all
@api_view(["DELETE"])
def delete_all_tenants(request):
    Tenant.objects.all().delete()
    return Response(
        {"message": "All tenants deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )
