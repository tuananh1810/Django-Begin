from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from customer.models import Customer
from decimal import Decimal
import uuid
from django.core.mail import send_mail


# Trả về đầy đủ thông tin Product
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  #liên kết serializer với model Product
        fields = [
            'id', 'code', 'name', 'quantity', 'price',
            'manufacture_date', 'expiry_date', 'created_by', 'created_at'
        ]  #liệt kê các trường bạn muốn trả về trong JSON


# OrderItem: nhập product là ID, trả về đầy đủ thông tin
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_detail = ProductDetailSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_detail', 'quantity', 'price', 'discount']


# Order: nhập customer là ID, trả về đầy đủ product trong items
class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'code', 'customer', 'total', 'created_at', 'items']
        read_only_fields = ['id', 'code', 'total', 'created_at']

    def generate_code(self):
        return "DH" + uuid.uuid4().hex[:6].upper()

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(
            code=self.generate_code(),
            total=Decimal('0.00'),
            **validated_data
        )

        total = Decimal('0.00')
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = Decimal(str(item_data['price']))
            discount = Decimal(str(item_data.get('discount', 0)))

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                discount=discount
            )

            total += (price - discount) * quantity

        order.total = total
        order.save()

        # Gửi email xác nhận đơn hàng cho khách hàng
        customer = order.customer
        subject = 'Đặt hàng thành công'
        message = f"""\
Xin chào {customer.name},
Mã đơn hàng: {order.code}
Tổng tiền: {order.total} VND

"""
        send_mail(
            subject,
            message,
            None,  # Email người gửi
            [customer.email],        # Gửi đến email khách hàng
            fail_silently=False
        )
        

        return order
