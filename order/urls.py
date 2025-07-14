from django.urls import path
from .views.views import (
    OrderListCreateView, OrderDetailView,
    OrderItemListCreateView, OrderItemDetailView
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    
    path('orders/<int:order_id>/items/', OrderItemListCreateView.as_view()),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view()),
]
