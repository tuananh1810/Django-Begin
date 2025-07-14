from django.db import models

class Customer(models.Model):
    code = models.CharField(max_length=20, unique=True)  # mã khách hàng
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # thời gian tạo

    def __str__(self):
        return f"{self.code} - {self.name}"
