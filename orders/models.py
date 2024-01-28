from django.db import models
from django.contrib.auth.models import User
import uuid
from products.models import Product


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    totalBill = models.FloatField()


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.IntegerField()
