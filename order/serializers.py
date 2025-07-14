from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from customer.models import Customer
from decimal import Decimal


class OrderItemSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(write_only=True)
    product = serializers.SerializerMethodField(read_only=True)  # để trả lại mã SP khi GET

    class Meta:
        model = OrderItem
        fields = ['product_code', 'product', 'quantity', 'price', 'discount']

    def get_product(self, obj):
        return obj.product.code if obj.product else None

    def create(self, validated_data):
        product_code = validated_data.pop('product_code')
        order = self.context.get('order')

        if not order:
            raise serializers.ValidationError("Không có thông tin đơn hàng để tạo OrderItem.")

        try:
            product = Product.objects.get(code=product_code)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Sản phẩm với mã '{product_code}' không tồn tại.")

        return OrderItem.objects.create(order=order, product=product, **validated_data)

class OrderSerializer(serializers.ModelSerializer):
    customer_code = serializers.CharField(write_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'code', 'customer_code', 'total', 'created_at', 'items']
        read_only_fields = ['total', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        customer_code = validated_data.pop('customer_code')

        if not items_data:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất 1 sản phẩm.")

        try:
            customer = Customer.objects.get(code=customer_code)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(f"Khách hàng với mã '{customer_code}' không tồn tại.")

        # Tạo đơn hàng trước
        order = Order.objects.create(**validated_data, customer=customer, total=Decimal('0.00'))

        total = Decimal('0.00')
        for item_data in items_data:
            serializer = OrderItemSerializer(data=item_data, context={"order": order})
            serializer.is_valid(raise_exception=True)
            item = serializer.save()
            total += Decimal(item.price) * item.quantity - Decimal(item.discount)

        order.total = total
        order.save()

        return order