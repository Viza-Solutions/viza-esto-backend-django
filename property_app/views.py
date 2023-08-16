from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound
from rest_framework import status

import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def property_list(request):
    properties = Property.objects.filter(deleted=False).order_by("name")
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_property_list(request, client_id):
    properties = Property.objects.filter(deleted=False, client_id=client_id).order_by(
        "name"
    )
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
    rooms = Room.objects.filter(deleted=False).order_by("room_number")
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_room_list(request, client_id):
    rooms = Room.objects.filter(deleted=False, client_id=client_id).order_by(
        "room_number"
    )
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def property_room_list(request, property_id):
    rooms = Room.objects.filter(deleted=False, property_id=property_id).order_by(
        "room_number"
    )
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def property_available_room_list(request, property_id):
    try:
        rooms = Room.objects.filter(
            deleted=False, property_id=property_id, is_available=True
        ).order_by("room_number")
        if not rooms.exists():
            raise NotFound("No available rooms for the given property.")

        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["DELETE"])
def delete_all_properties(request):
    Property.objects.all().delete()
    return Response(
        {"message": "All properties deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["POST"])
def create_room(request):
    request.data["added_by"] = request.user.id
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
    return Response(
        {"message": "All rooms deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


# ROOM TPER?
# Create RoomType
@api_view(["POST"])
def create_room_type(request):
    serializer = RoomTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(added_by=request.user)
        return Response(
            {"message": "Room type created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Read (List) RoomTypes
@api_view(["GET"])
def list_room_types(request):
    room_types = RoomType.objects.all().order_by("name")
    serializer = RoomTypeSerializer(room_types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Read (Retrieve) RoomType
@api_view(["GET"])
def retrieve_room_type(request, room_type_id):
    try:
        room_type = RoomType.objects.get(pk=room_type_id)
    except RoomType.DoesNotExist:
        return Response(
            {"message": "Room type not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = RoomTypeSerializer(room_type)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Update RoomType
@api_view(["PUT"])
def update_room_type(request, room_type_id):
    try:
        room_type = RoomType.objects.get(pk=room_type_id)
    except RoomType.DoesNotExist:
        return Response(
            {"message": "Room type not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = RoomTypeSerializer(room_type, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Room type updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete RoomType
@api_view(["DELETE"])
def delete_room_type(request, room_type_id):
    try:
        room_type = RoomType.objects.get(pk=room_type_id)
    except RoomType.DoesNotExist:
        return Response(
            {"message": "Room type not found"}, status=status.HTTP_404_NOT_FOUND
        )

    room_type.delete()
    return Response(
        {"message": "Room type deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


# csv

from rest_framework.decorators import authentication_classes, permission_classes

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def export_room_csv_headers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="room_headers.csv"'

    writer = csv.writer(response)
    headers = ['Room Number', 'Floor', 'Description', 'Room Type',
               'Bedrooms', 'Bathrooms', 'Size', 'Monthly Price']
    writer.writerow(headers)

    return response


@api_view(['GET'])
def export_property_csv_headers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="property_headers.csv"'

    writer = csv.writer(response)
    headers = ['Name', 'Country', 'Town', 'Address', 'Description',
               'Rooms', 'Status']
    writer.writerow(headers)

    return response