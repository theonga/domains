from .views import BlogView, BlogDetailView
from django.urls import path, include

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='article-detail'),
]
