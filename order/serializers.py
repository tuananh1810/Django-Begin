from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from customer.models import Customer

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Product.objects.all()
    )
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'price']
        read_only_fields = ['price', 'product_name']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Customer.objects.all()
    )

    class Meta:
        model = Order
        fields = ['id', 'code', 'customer', 'total', 'created_at', 'items']
        read_only_fields = ['total', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        if not items_data:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất 1 sản phẩm.")

        total = 0
        order = Order.objects.create(**validated_data, total=0)

        for item in items_data:
            product_id = item['product'].id
            quantity = item['quantity']

            if quantity <= 0:
                continue  # Bỏ qua sản phẩm có số lượng <= 0

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Sản phẩm với ID {product_id} không tồn tại."
                )

            if product.quantity < quantity:
                raise serializers.ValidationError(
                    f"Sản phẩm '{product.name}' không đủ hàng trong kho (còn {product.quantity})."
                )

            price = product.price
            total += price * quantity

            product.quantity -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        order.total = total
        order.save()
        return order
