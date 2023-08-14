from django.shortcuts import render

from property_app.models import *
from tenant_app.models import *
from issue_notice_app.models import *
from datetime import date, timedelta

from expense_app.models import *
from datetime import datetime
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes


# Create your views here.


# room count
def client_room_counts(client_id):
    available_count = Room.objects.filter(
        client_id=client_id, is_available=True
    ).count()
    unavailable_count = Room.objects.filter(
        client_id=client_id, is_available=False
    ).count()

    counts = {
        "available_count": available_count,
        "unavailable_count": unavailable_count,
    }
    return counts


def property_room_counts(property_id):
    available_count = Room.objects.filter(
        property_id=property_id, is_available=True
    ).count()
    unavailable_count = Room.objects.filter(
        property_id=property_id, is_available=False
    ).count()
    counts = {
        "available_count": available_count,
        "unavailable_count": unavailable_count,
    }
    return counts


# lease count
def client_expiring_leases_count(client_id):
    today = date.today()
    two_months_later = today + timedelta(days=2 * 30)

    expiring_leases_count = Tenant.objects.filter(
        date_of_lease__range=[today, two_months_later],
        deleted=False,
        client_id=client_id,
    ).count()

    return expiring_leases_count


def property_expiring_leases_count(property_id):
    today = date.today()
    two_months_later = today + timedelta(days=2 * 30)

    expiring_leases_count = Tenant.objects.filter(
        date_of_lease__range=[today, two_months_later],
        deleted=False,
        property_id=property_id,
    ).count()

    return expiring_leases_count


# notices
def get_active_notice_count_property(property_id):
    active_notice_count = TenantNotice.objects.filter(
        is_active=True, property_id=property_id, date_to_vacate__gte=date.today()
    ).count()
    return active_notice_count


def get_active_notice_count_client(client_id):
    active_notice_count = TenantNotice.objects.filter(
        is_active=True, client_id=client_id, date_to_vacate__gte=date.today()
    ).count()
    return active_notice_count


# issues
def get_open_issue_count(client_id):
    open_issue_count = EstateIssue.objects.filter(
        is_open=True, client_id=client_id
    ).count()
    return open_issue_count


def get_open_issue_count(property_id):
    open_issue_count = EstateIssue.objects.filter(
        is_open=True, property_id=property_id
    ).count()
    return open_issue_count


# expenses
def client_total_expenses_for_current_month(client_id):
    current_month = datetime.now().month
    current_year = datetime.now().year

    total_expenses = (
        Expense.objects.filter(
            date__year=current_year, date__month=current_month, client_id=client_id
        ).aggregate(models.Sum("amount"))["amount__sum"]
        or 0.00
    )

    return total_expenses


def property_total_expenses_for_current_month(property_id):
    current_month = datetime.now().month
    current_year = datetime.now().year

    total_expenses = (
        Expense.objects.filter(
            date__year=current_year, date__month=current_month, linked_property=property_id
        ).aggregate(models.Sum("amount"))["amount__sum"]
        or 0.00
    )

    return total_expenses


@api_view(["GET"])
def fetch_dashboard_data_client(request, client_id):
    room_counts = client_room_counts(client_id)
    expiring_leases_count = client_expiring_leases_count(client_id)
    active_notice_count = get_active_notice_count_client(client_id)
    open_issue_count = get_open_issue_count(client_id)
    total_expenses = client_total_expenses_for_current_month(client_id)

    data = {
        "room_counts": room_counts,
        "expiring_leases_count": expiring_leases_count,
        "active_notice_count": active_notice_count,
        "open_issue_count": open_issue_count,
        "total_expenses": total_expenses,
    }

    return Response(data)


@api_view(["GET"])
def fetch_dashboard_data_property(request, property_id):
    room_counts = property_room_counts(property_id)
    expiring_leases_count = property_expiring_leases_count(property_id)
    active_notice_count = get_active_notice_count_property(property_id)
    open_issue_count = get_open_issue_count(property_id)
    total_expenses = property_total_expenses_for_current_month(property_id)

    data = {
        "room_counts": room_counts,
        "expiring_leases_count": expiring_leases_count,
        "active_notice_count": active_notice_count,
        "open_issue_count": open_issue_count,
        "total_expenses": total_expenses,
    }

    return Response(data)
