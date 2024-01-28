from django.db import models
import uuid


# Create your models here.
class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name
