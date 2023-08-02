from django.urls import path
from . import views

urlpatterns = [
    path('sms_to_all_tenants/<int:client_id>', views.sms_to_all_tenants, name='sms_to_all_tenants'),
    path('sms_to_property_tenants/<int:property_id>', views.sms_to_property_tenants, name='sms_to_property_tenants'),
]
