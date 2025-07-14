# order/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Order, OrderItem
from ..serializers import OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated


# ----------- ORDER -------------
class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # thêm created_by=request.user nếu cần
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"detail": "Order not found"}, status=404)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"detail": "Order not found"}, status=404)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"detail": "Order not found"}, status=404)
        order.delete()
        return Response(status=204)


# ----------- ORDER ITEM -------------
class OrderItemListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order_items = OrderItem.objects.filter(order_id=order_id)
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    def post(self, request, order_id):
        data = request.data.copy()
        data['order'] = order_id
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrderItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return None

    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"detail": "OrderItem not found"}, status=404)
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"detail": "OrderItem not found"}, status=404)
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"detail": "OrderItem not found"}, status=404)
        item.delete()
        return Response(status=204)
