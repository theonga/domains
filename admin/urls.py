from .views import AdminView, ListView, InvoiceView, RegisteredDomainView, PaymentView, SearchDomain, delete_user, UpdateAccountView, TransferDomainView
from django.urls import path, include

urlpatterns = [
    path('', AdminView.as_view(), name='index'),
    path('new/', SearchDomain, name="new"),
    path('registered/', RegisteredDomainView.as_view(), name='registered'),
    path('payments/', PaymentView.as_view(), name='payments'),
    path('domain/<category>/', ListView.as_view(), name='list'),
    path('invoices/<int:pk>/', InvoiceView.as_view(), name="invoices"),
    path('update/<int:pk>/', UpdateAccountView.as_view(), name="update"),
    path('transfer/', TransferDomainView.as_view(), name="transfer"),
    path('delete/', delete_user, name="account_delete"),
]
