from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from drf_yasg.utils import swagger_auto_schema
from generic.swagger_example import post_order  # cấu trúc swagger
from general.general import convert_response  # format response chuẩn


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Order"],
        operation_id="Create Order with Items",
        operation_description="Tạo đơn hàng kèm theo danh sách sản phẩm",
        request_body=post_order,
        responses={201: "Created", 400: "Bad Request"}
    )
    @transaction.atomic
    def post(self, request):
        order_data = request.data.get("order")
        order_items_data = request.data.get("orderitem")

        if not order_data or not order_items_data:
            return Response(convert_response("Missing order or orderitem", 400))

        # Tạo Order
        order_serializer = OrderSerializer(data=order_data, context={"request": request})
        if not order_serializer.is_valid():
            return Response(convert_response("Invalid order", 400, order_serializer.errors))

        order_instance = order_serializer.save()

        # Tạo OrderItem
        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
        if not order_item_serializer.is_valid():
            order_instance.delete()
            return Response(convert_response("Invalid orderitem", 400, order_item_serializer.errors))

        order_items = order_item_serializer.save(order=order_instance)

        # Tính tổng tiền
        total = 0
        for item in order_items:
            total += item.price * item.quantity - item.discount
        order_instance.total = total
        order_instance.save()

        response_data = {
            "order": OrderSerializer(order_instance).data,
            "order_items": OrderItemSerializer(order_items, many=True).data
        }
        return Response(convert_response("Success", 201, response_data))
