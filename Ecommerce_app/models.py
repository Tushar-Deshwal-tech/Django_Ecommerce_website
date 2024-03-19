from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserData(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.PositiveIntegerField()
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=130)

    def __str__(self):
        return self.first_name

class OrderData(models.Model):
    order_by = models.CharField(max_length=30)
    order_number = models.PositiveIntegerField()
    order_status = models.CharField(max_length=30)
    total_item = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=30)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_time = models.DateTimeField()

class OrderItem(models.Model):
    order = models.ForeignKey(OrderData, related_name='order_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_quantity = models.PositiveIntegerField()
    item_size = models.CharField(max_length=10)
    item_color = models.CharField(max_length=20)

class ReviewData(models.Model):
    user_name = models.CharField(max_length=30)
    text = models.CharField(max_length=100)
    star = models.PositiveIntegerField()

