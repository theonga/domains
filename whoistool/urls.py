from .views import WhoisView
from django.urls import path, include

urlpatterns = [
    path('', WhoisView, name='whois'),
]
