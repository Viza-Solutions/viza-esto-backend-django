from django.urls import path
from . import views

urlpatterns = [
    path('expense-types', views.expense_type_list, name='expense-type-list'),
    path('expense-types/create', views.expense_type_create, name='expense-type-create'),
    path('expense-types/<int:pk>', views.expense_type_detail, name='expense-type-detail'),
    path('expense-types/by-parent', views.expense_type_list_by_parent, name='expense-type-list-by-parent'),
    path('expense-types/by-parent/<int:parent_id>', views.expense_type_list_by_parent, name='expense-type-list-by-parent-id'),
]
