from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path('', CustomerListCreateView.as_view()),         # /api/customers/
    path('<int:pk>/', CustomerDetailView.as_view()),    # /api/customers/1/
]
