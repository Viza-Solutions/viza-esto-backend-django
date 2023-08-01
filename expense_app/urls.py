from django.urls import path
from . import views

urlpatterns = [
    # ExpenseType URLs
    path('expense-types/', views.expense_type_list, name='expense-type-list'),
    path('expense-types/create/', views.expense_type_create, name='expense-type-create'),
    path('expense-types/<int:pk>/', views.expense_type_detail, name='expense-type-detail'),
    path('expense-types/by-parent/', views.expense_type_list_by_parent, name='expense-type-list-by-parent'),
    path('expense-types/by-parent/<int:parent_id>/', views.expense_type_list_by_parent, name='expense-type-list-by-parent-id'),

    # Expense URLs
    path('expenses/<int:pk>/', views.retrieve_expense, name='retrieve-expense'),
    path('expenses/', views.create_expense, name='create-expense'),
    path('expenses/update/<int:pk>/', views.update_expense, name='update-expense'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete-expense'),
    path('expenses/by-property/<int:property_id>/', views.get_expenses_by_property, name='expenses-by-property'),
    path('expenses/by-client/<int:client_id>/', views.get_expenses_by_client, name='expenses-by-client'),
]
