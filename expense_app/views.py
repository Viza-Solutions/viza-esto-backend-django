from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ExpenseType
from .serializers import ExpenseTypeSerializer


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
