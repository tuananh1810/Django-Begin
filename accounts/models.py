from django.db import models
from django.contrib.auth.models import AbstractUser

class Permission(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):  # Kế thừa User mặc định
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def has_permission(self, code):
        if self.role:
            return self.role.permissions.filter(code=code).exists()
        return False
