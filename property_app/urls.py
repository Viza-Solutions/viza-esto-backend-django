from django.urls import path
from .views import *

urlpatterns = [
    path("properties", property_list, name="property-list"),
    path("properties/create", create_property, name="property-create"),
    path("properties/<int:pk>", retrieve_property, name="property-retrieve"),
    path("properties/update/<int:pk>", update_property, name="property-update"),
    path("properties/delete/<int:pk>", delete_property, name="property-delete"),

    path('clients-properties/<int:client_id>', client_property_list, name='client-property-list'),

    # rooms

    path('rooms', room_list, name='room-list'),
    path('rooms/create', create_room, name='create-room'),
    path('rooms/<int:pk>', retrieve_room, name='retrieve-room'),
    path('rooms/update/<int:pk>', update_room, name='update-room'),
    path('rooms/delete/<int:pk>', delete_room, name='delete-room'),

    path('clients/rooms/<int:client_id>', client_room_list, name='client-room-list'),
    path('properties/rooms/<int:property_id>', property_room_list, name='property-room-list'),

    path('rooms/delete-all', delete_all_rooms, name='delete-all-rooms'),

    # RoomTypes CRUD URLs

    path('  ', create_room_type, name='create-room-type'),
    path('roomtypes/<int:room_type_id>', retrieve_room_type, name='retrieve-room-type'),
    path('roomtypes/update/<int:room_type_id>', update_room_type, name='update-room-type'),
    path('roomtypes/delete/<int:room_type_id>', delete_room_type, name='delete-room-type'),
    path('roomtypes/list', list_room_types, name='list-room-types'),
]
