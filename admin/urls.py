from .views import AdminView, Manage,  DomainListView, InvoiceView, MakePayment, RegisteredDomainView, PaymentView, SearchDomain, delete_user, UpdateAccountView, TransferDomainView
from django.urls import path, include

urlpatterns = [
    path('', AdminView.as_view(), name='index'),
    path('new/', SearchDomain, name="new"),
    path('manage/<int:pk>/', Manage.as_view(), name="manage"),
    path('registered/', RegisteredDomainView.as_view(), name='registered'),
    path('pay/<domain>/', MakePayment.as_view(), name='pay'),
    path('payments/', PaymentView.as_view(), name='payments'),
    path('domain/<status>/', DomainListView.as_view(), name='list'),
    path('update/<int:pk>/', UpdateAccountView.as_view(), name="update"),
    path('transfer/', TransferDomainView.as_view(), name="transfer"),
    path('delete/', delete_user, name="account_delete"),
]
