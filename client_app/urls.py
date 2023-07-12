from django.urls import path
from .views import client_list, create_client, retrieve_client, update_client, delete_client

urlpatterns = [
    path('clients', client_list, name='client-list'),
    path('clients/create', create_client, name='client-create'),
    path('clients/<int:pk>', retrieve_client, name='client-retrieve'),
    path('clients/update/<int:pk>', update_client, name='client-update'),
    path('clients/delete/<int:pk>', delete_client, name='client-delete'),
]