from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

from datetime import date


# Create
@api_view(["POST"])
def create_estate_issue(request):
    if request.method == "POST":
        serializer = EstateIssueSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Estate issue created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Failed to create estate issue.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Read
@api_view(["GET"])
def get_estate_issue(request, issue_id):
    try:
        issue = EstateIssue.objects.get(pk=issue_id)
    except EstateIssue.DoesNotExist:
        return Response(
            {"message": "Estate issue not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = EstateIssueSerializer(issue)
    return Response(
        {"message": "Estate issue retrieved successfully.", "data": serializer.data}
    )


# Update
@api_view(["PUT"])
def update_estate_issue(request, issue_id):
    try:
        issue = EstateIssue.objects.get(pk=issue_id)
    except EstateIssue.DoesNotExist:
        return Response(
            {"message": "Estate issue not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = EstateIssueSerializer(issue, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Estate issue updated successfully.", "data": serializer.data}
        )
    return Response(
        {"message": "Failed to update estate issue.", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["PUT"])
def close_estate_issue(request, issue_id):
    try:
        issue = EstateIssue.objects.get(pk=issue_id)
    except EstateIssue.DoesNotExist:
        return Response(
            {"message": "Estate issue not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if issue.is_open:
        issue.is_open = False
        issue.closed_by = request.user  # Assuming you're using authentication

        issue.save()

        return Response(
            {"message": "Estate issue closed successfully."},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": "Estate issue is already closed."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Delete
@api_view(["DELETE"])
def delete_estate_issue(request, issue_id):
    try:
        issue = EstateIssue.objects.get(pk=issue_id)
    except EstateIssue.DoesNotExist:
        return Response(
            {"message": "Estate issue not found."}, status=status.HTTP_404_NOT_FOUND
        )

    issue.delete()
    return Response(
        {"message": "Estate issue deleted successfully."},
        status=status.HTTP_204_NO_CONTENT,
    )


# ...


@api_view(["GET"])
def get_unresolved_issues_for_property(request, property_id):
    try:
        property_ = Property.objects.get(pk=property_id)
    except Property.DoesNotExist:
        return Response(
            {"message": "Property not found."}, status=status.HTTP_404_NOT_FOUND
        )

    unresolved_issues = EstateIssue.objects.filter(property=property_, is_open=True)
    serializer = EstateIssueSerializer(unresolved_issues, many=True)
    return Response(
        {
            "message": "Unresolved issues retrieved successfully.",
            "data": serializer.data,
        }
    )


@api_view(["GET"])
def get_unresolved_issues_for_client(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return Response(
            {"message": "Client not found."}, status=status.HTTP_404_NOT_FOUND
        )

    unresolved_issues = EstateIssue.objects.filter(client=client, is_open=True)
    serializer = EstateIssueSerializer(unresolved_issues, many=True)
    return Response(
        {
            "message": "Unresolved issues for the client retrieved successfully.",
            "data": serializer.data,
        }
    )


# TENANT NOTICES
# Create
@api_view(["POST"])
def create_tenant_notice(request):
    if request.method == "POST":
        serializer = TenantNoticeSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Tenant notice created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Failed to create tenant notice.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Read
@api_view(["GET"])
def get_tenant_notice(request, notice_id):
    try:
        notice = TenantNotice.objects.get(pk=notice_id)
    except TenantNotice.DoesNotExist:
        return Response(
            {"message": "Tenant notice not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = TenantNoticeSerializer(notice)
    return Response(
        {"message": "Tenant notice retrieved successfully.", "data": serializer.data}
    )


# Update
@api_view(["PUT"])
def update_tenant_notice(request, notice_id):
    try:
        notice = TenantNotice.objects.get(pk=notice_id)
    except TenantNotice.DoesNotExist:
        return Response(
            {"message": "Tenant notice not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = TenantNoticeSerializer(notice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Tenant notice updated successfully.", "data": serializer.data}
        )
    return Response(
        {"message": "Failed to update tenant notice.", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# Delete
@api_view(["DELETE"])
def delete_tenant_notice(request, notice_id):
    try:
        notice = TenantNotice.objects.get(pk=notice_id)
    except TenantNotice.DoesNotExist:
        return Response(
            {"message": "Tenant notice not found."}, status=status.HTTP_404_NOT_FOUND
        )

    notice.delete()
    return Response(
        {"message": "Tenant notice deleted successfully."},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["GET"])
def pending_notices(request):
    current_date = date.today()
    pending_notices = TenantNotice.objects.filter(
        date_to_vacate__gte=current_date
    ).order_by("date_to_vacate")

    serializer = TenantNoticeSerializer(pending_notices, many=True)
    return Response(
        {
            "message": "Pending notices retrieved successfully.",
            "data": serializer.data,
        }
    )
