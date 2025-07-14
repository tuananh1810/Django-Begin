from django.db import models
from django.conf import settings

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)  # mã sản phẩm
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)  # số lượng sản phẩm
    price = models.DecimalField(max_digits=12, decimal_places=2)
    manufacture_date = models.DateField(null=True, blank=True)  # ngày sản xuất
    expiry_date = models.DateField(null=True, blank=True)       # hạn sử dụng
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"



