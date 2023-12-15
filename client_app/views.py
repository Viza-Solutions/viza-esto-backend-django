from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer
from rest_framework import status

@api_view(["GET"])
def client_list(request):
    clients = Client.objects.filter(deleted=False)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

 
@api_view(["POST"])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Client created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_client(request, pk):
    try:
        client = Client.objects.get(pk=pk, deleted=False)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    except Client.DoesNotExist:
        return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk, deleted=False)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Client updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Client.DoesNotExist:
        return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk, deleted=False)
        client.deleted = True  # Set deleted field to True
        client.save()
        return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Client.DoesNotExist:
        return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
