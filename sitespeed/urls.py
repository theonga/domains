from .views import SiteSpeedView
from django.urls import path, include

urlpatterns = [
    path('', SiteSpeedView, name='sitespeed'),
]
