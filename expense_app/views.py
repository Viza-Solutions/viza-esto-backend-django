from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def expense_type_list(request):
    """
    List all ExpenseTypes.
    """
    expense_types = ExpenseType.objects.all()
    serializer = ExpenseTypeSerializer(expense_types, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def expense_type_create(request):
    """
    Create a new ExpenseType.
    """
    serializer = ExpenseTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def expense_type_detail(request, pk):
    """
    Retrieve, update, or delete an ExpenseType.
    """
    try:
        expense_type = ExpenseType.objects.get(pk=pk)
    except ExpenseType.DoesNotExist:
        return Response({"detail": "ExpenseType not found."}, status=404)

    if request.method == "GET":
        serializer = ExpenseTypeSerializer(expense_type)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ExpenseTypeSerializer(expense_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        expense_type.delete()
        return Response(status=204)


@api_view(["GET"])
def expense_type_list_by_parent(request, parent_id=None):
    """
    List ExpenseTypes based on parent ID or list all ExpenseTypes without a parent.
    """
    if parent_id is None:
        expense_types = ExpenseType.objects.filter(parent=None)
    else:
        expense_types = ExpenseType.objects.filter(parent_id=parent_id)

    serializer = ExpenseTypeSerializer(expense_types, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def retrieve_expense(request, pk):
    """
    Retrieve a single expense by its primary key (ID).
    """
    expense = get_object_or_404(Expense, pk=pk)
    serializer = ExpenseSerializer(expense)
    return Response(
        {"message": "Expense retrieved successfully", "data": serializer.data}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_expense(request):
    """
    Create a new expense.
    """
    serializer = ExpenseSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Expense created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"message": "Invalid data", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["PUT"])
def update_expense(request, pk):
    """
    Update an existing expense identified by its primary key (ID).
    """
    expense = get_object_or_404(Expense, pk=pk)
    serializer = ExpenseSerializer(expense, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Expense updated successfully", "data": serializer.data}
        )
    return Response(
        {"message": "Invalid data", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["DELETE"])
def delete_expense(request, pk):
    """
    Delete an existing expense identified by its primary key (ID).
    """
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return Response(
        {"message": "Expense deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


@api_view(["GET"])
def get_expenses_by_property(request, property_id):
    """
    Get all expenses associated with a particular property.
    """
    expenses = Expense.objects.filter(linked_property_id=property_id)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(
        {"message": "Expenses retrieved successfully", "data": serializer.data}
    )


@api_view(["GET"])
def get_expenses_by_client(request, client_id):
    """
    Get all expenses associated with a particular client.
    """
    expenses = Expense.objects.filter(client_id=client_id)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(
        {"message": "Expenses retrieved successfully", "data": serializer.data}
    )
