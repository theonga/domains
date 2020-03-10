from .views import HomePageView, AboutPageView, Register,Contact
from django.urls import path, include

urlpatterns = [
    path('', HomePageView, name='home'),
    path('contact/', Contact, name='contact'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('register/<domain>/', Register.as_view(), name='register'),
]
