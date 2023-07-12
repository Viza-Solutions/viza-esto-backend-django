from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status


@api_view(["GET"])
def property_list(request):
    properties = Property.objects.filter(deleted=False)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_property_list(request, client_id):
    properties = Property.objects.filter(deleted=False, client_id=client_id)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_property(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(added_by=request.user)
        return Response(
            {"message": "Property created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_property(request, pk):
    try:
        property_ = Property.objects.get(pk=pk, deleted=False)
        serializer = PropertySerializer(property_)
        return Response(serializer.data)
    except Property.DoesNotExist:
        return Response(
            {"message": "Property not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
def update_property(request, pk):
    try:
        property_ = Property.objects.get(pk=pk, deleted=False)
        serializer = PropertySerializer(property_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Property updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Property.DoesNotExist:
        return Response(
            {"message": "Property not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
def delete_property(request, pk):
    try:
        property_ = Property.objects.get(pk=pk, deleted=False)
        property_.deleted = True
        property_.save()
        return Response(
            {"message": "Property deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Property.DoesNotExist:
        return Response(
            {"message": "Property not found"}, status=status.HTTP_404_NOT_FOUND
        )


# room
@api_view(["GET"])
def room_list(request):
    rooms = Room.objects.filter(deleted=False)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_room_list(request, client_id):
    rooms = Room.objects.filter(deleted=False, client_id=client_id)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def property_room_list(request, property_id):
    rooms = Room.objects.filter(deleted=False, property_id=property_id)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Room created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_room(request, pk):
    try:
        room = Room.objects.get(pk=pk, deleted=False)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except Room.DoesNotExist:
        return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def update_room(request, pk):
    try:
        room = Room.objects.get(pk=pk, deleted=False)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Room updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Room.DoesNotExist:
        return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_room(request, pk):
    try:
        room = Room.objects.get(pk=pk, deleted=False)
        room.deleted = True
        room.save()
        return Response(
            {"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
    except Room.DoesNotExist:
        return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)



# delete-all

@api_view(["DELETE"])
def delete_all_rooms(request):
    Room.objects.all().delete()
    return Response({"message": "All rooms deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
