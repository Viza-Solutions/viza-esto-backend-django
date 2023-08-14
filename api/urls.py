from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("client/", include("client_app.urls")),
    path("property/", include("property_app.urls")),
    path("tenant/", include("tenant_app.urls")),
    path("payment/", include("payment_app.urls")),
    path("expense/", include("expense_app.urls")),
    path("issue-notice/", include("issue_notice_app.urls")),
    path("sms/", include("sms_api.urls")),
    path("dashboard/", include("dashboard_app.urls")),
]
