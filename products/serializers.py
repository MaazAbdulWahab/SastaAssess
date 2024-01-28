from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializerDescription(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_id", "name"]
