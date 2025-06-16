from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('ajouter/', views.expense_create, name='expense_create'),
    path('historique/', views.transaction_list, name='transaction_list'),
    path('<int:pk>/modifier/', views.expense_update, name='expense_update'),
    path('<int:pk>/supprimer/', views.expense_delete, name='expense_delete'),
    path('list/', views.transaction_list, name='transaction_list'),
    # ... autres URLs
]
