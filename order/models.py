from django.db import models
from customer.models import Customer
from product.models import Product
from django.db.models import PROTECT

class Order(models.Model):
    code = models.CharField(max_length=20, unique=True)  # mã đơn hàng
    customer = models.ForeignKey(Customer, on_delete=PROTECT)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # thời gian tạo

    def __str__(self):
        return self.code


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)  # đơn giá

    def __str__(self):
        return f"{self.order.code} - {self.product.code}"
