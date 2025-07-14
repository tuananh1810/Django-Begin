from django.urls import path
from .views.views import (
    OrderListCreateView, OrderDetailView,
    OrderItemListCreateView, OrderItemDetailView
)

urlpatterns = [
   
    path('', OrderListCreateView.as_view()),
    path('<int:pk>/', OrderDetailView.as_view()),
    path('<int:order_id>/items/', OrderItemListCreateView.as_view()),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view()),
]
