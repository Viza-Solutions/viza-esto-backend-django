from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from django.db import IntegrityError


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
