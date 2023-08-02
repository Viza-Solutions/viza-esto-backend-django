from django.urls import path
from . import views

urlpatterns = [
    # Estate Issue URLs
    path('issue/create', views.create_estate_issue, name='create-estate-issue'),
    path('issue/get/<int:issue_id>', views.get_estate_issue, name='get-estate-issue'),
    path('issue/update/<int:issue_id>', views.update_estate_issue, name='update-estate-issue'),
    path('issue/delete/<int:issue_id>', views.delete_estate_issue, name='delete-estate-issue'),
    path('unresolved-issues-for-property/<int:property_id>', views.get_unresolved_issues_for_property, name='unresolved-issues-for-property'),
    path('unresolved-issues-for-client/<int:client_id>', views.get_unresolved_issues_for_client, name='unresolved-issues-for-client'),
    path('close-issue/<int:issue_id>', views.close_estate_issue, name='close_estate_issue'),
    
    # Tenant Notice URLs
    path('notice/create', views.create_tenant_notice, name='create-tenant-notice'),
    path('notice/get/<int:notice_id>', views.get_tenant_notice, name='get-tenant-notice'),
    path('notice/update/<int:notice_id>', views.update_tenant_notice, name='update-tenant-notice'),
    path('notice/delete/<int:notice_id>', views.delete_tenant_notice, name='delete-tenant-notice'),
    path('notices/pending-notices', views.pending_notices, name='pending-notices'),
    path('notices/close/<int:notice_id>', views.close_tenant_notice, name='close_tenant_notice'),
]
