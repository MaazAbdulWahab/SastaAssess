from rest_framework import serializers
from products.serializers import ProductSerializerDescription


class Requests(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderPlacement(serializers.Serializer):
    requests = serializers.ListField(child=Requests(), min_length=1)


class OrderItemsSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product = ProductSerializerDescription()


class OrderRetrieveSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    placed_at = serializers.DateTimeField()
    totalBill = serializers.FloatField()
    items = OrderItemsSerializer(many=True)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()


class OrderRetrieveSerializerWithUserInfo(OrderRetrieveSerializer):
    user = UserSerializer()
