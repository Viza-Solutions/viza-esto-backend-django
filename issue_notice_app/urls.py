from django.urls import path
from . import views

urlpatterns = [
    path('estate-issues/create/', views.create_estate_issue, name='create_estate_issue'),
    path('estate-issues/<int:issue_id>', views.get_estate_issue, name='get_estate_issue'),
    path('estate-issues/update/<int:issue_id>', views.update_estate_issue, name='update_estate_issue'),
    path('estate-issues/delete/<int:issue_id>', views.delete_estate_issue, name='delete_estate_issue'),
    path('property/unresolved-issues/<int:property_id>', views.get_unresolved_issues_for_property, name='get_unresolved_issues_for_property'),
    path('client/unresolved-issues/<int:client_id>', views.get_unresolved_issues_for_client, name='get_unresolved_issues_for_client'),
]
