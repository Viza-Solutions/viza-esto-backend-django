from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from django.db import IntegrityError

from datetime import datetime
from uuid import uuid4


# Views
@api_view(["GET"])
def payment_method_list(request):
    payment_methods = PaymentMethod.objects.filter(deleted=False)
    serializer = PaymentMethodSerializer(payment_methods, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_payment_method_list(request, client_id):
    payment_methods = PaymentMethod.objects.filter(deleted=False, client_id=client_id)
    serializer = PaymentMethodSerializer(payment_methods, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_payment_method(request):
    serializer = PaymentMethodSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(added_by=request.user)
            return Response(
                {
                    "message": "Payment method created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {
                    "error": "A payment method with the same name already exists for this client."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_payment_method(request, pk):
    try:
        payment_method = PaymentMethod.objects.get(pk=pk, deleted=False)
        serializer = PaymentMethodSerializer(payment_method)
        return Response(serializer.data)
    except PaymentMethod.DoesNotExist:
        return Response(
            {"message": "Payment method not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
def update_payment_method(request, pk):
    try:
        payment_method = PaymentMethod.objects.get(pk=pk, deleted=False)
        serializer = PaymentMethodSerializer(
            payment_method, data=request.data, partial=True
        )
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {
                        "message": "Payment method updated successfully",
                        "data": serializer.data,
                    }
                )
            except IntegrityError:
                return Response(
                    {
                        "error": "A payment method with the same name already exists for this client."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PaymentMethod.DoesNotExist:
        return Response(
            {"message": "Payment method not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
def delete_payment_method(request, pk):
    try:
        payment_method = PaymentMethod.objects.get(pk=pk, deleted=False)
        payment_method.deleted = True
        payment_method.save()
        return Response(
            {"message": "Payment method deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    except PaymentMethod.DoesNotExist:
        return Response(
            {"message": "Payment method not found"}, status=status.HTTP_404_NOT_FOUND
        )


# PAYMENT
@api_view(["POST"])
def create_payment_transaction(request):
    serializer = PaymentTransactionSerializer(data=request.data)
    if serializer.is_valid():
        tenant_id = serializer.validated_data["tenant"].id

        # Retrieve tenant and room price in a single query
        tenant = Tenant.objects.select_related("room", "client").get(pk=tenant_id)
        room_price = tenant.room.monthly_price

        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year

        payment_transactions = PaymentTransaction.objects.filter(
            tenant=tenant
        ).order_by("-created_at")

        if payment_transactions.exists():
            first_payment_transaction = payment_transactions.first()
            last_paid_month = first_payment_transaction.month
            last_paid_year = first_payment_transaction.year

            unpaid_months = (
                (current_year - last_paid_year) * 12 + current_month - last_paid_month
            )
            rent_to_be_paid = unpaid_months * room_price

            new_balance = serializer.validated_data["amount"] - (
                rent_to_be_paid - first_payment_transaction.balance
            )
        else:
            new_balance = serializer.validated_data["amount"] - room_price

        # Validate the client ID
        client_id = serializer.validated_data["client"].id
        if tenant.client_id != client_id:
            return Response(
                {
                    "error": "Invalid client id provided. The client does not match the tenant."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate a unique UUID
        uuid = str(uuid4())

        serializer.save(
            balance=new_balance,
            month=current_month,
            year=current_year,
            uuid=uuid,
        )
        return Response(
            {
                "message": "Payment transaction created successfully",
                "receipt_number": serializer.data["id"],
                "balance": serializer.data["balance"],
                # all the data
                # "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_all_payment_transactions(request):
    # Delete all payment transactions
    PaymentTransaction.objects.all().delete()
    return Response(
        {"message": "All payment transactions deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )



# reports

# views.py
import openpyxl
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PaymentTransaction
from openpyxl.chart import BarChart, Reference


@api_view(["GET"])
def excel_report_view(request, tenant_id):
    # Retrieve the data from the PaymentTransaction model for the specific Tenant
    queryset = PaymentTransaction.objects.filter(tenant_id=tenant_id)

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f"Payment Transactions Report - Tenant {tenant_id}"

    # Write the header row with bold font, centered alignment, and font color
    header_font = openpyxl.styles.Font(bold=True)
    header_alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")

    headers = [
        "ID",
        "Amount",
        "Balance",
        "Month",
        "Year",
        "Payment Method",
        "Reference",
        "Description",
        "Processed By",
        "Client",
        "Reversed",
        "UUID",
        "Created At",
        "Updated At",
    ]
    for col_num, header in enumerate(headers, start=1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = header.upper()  # Capitalize the header
        cell.font = header_font
        cell.alignment = header_alignment

    # Write data rows
    data_alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
    for row_num, transaction in enumerate(queryset, start=2):
        data = [
            transaction.id,
            transaction.amount,
            transaction.balance,
            transaction.month,
            transaction.year,
            str(transaction.payment_method),
            transaction.reference,
            transaction.description,
            str(transaction.processed_by),
            str(transaction.client),
            transaction.reversed,
            str(transaction.uuid),
            transaction.created_at,
            transaction.updated_at,
        ]
        for col_num, value in enumerate(data, start=1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = value
            cell.alignment = data_alignment

    # Auto-fit column width for all columns
    for col_num, header in enumerate(headers, start=1):
        column_letter = openpyxl.utils.get_column_letter(col_num)
        worksheet.column_dimensions[column_letter].auto_size = True

    # Create a response with the Excel file
    response = Response(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f"attachment; filename=tenant_{tenant_id}_report.xlsx"
    workbook.save(response)

    return response
