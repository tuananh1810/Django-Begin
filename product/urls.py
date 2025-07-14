from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductView



urlpatterns = [
    path('', ProductView.as_view()),  # /api/products/
]