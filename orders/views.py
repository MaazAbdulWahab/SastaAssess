from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, OrderItems
from orders.serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from products.models import Product
from rest_framework.views import APIView
from utils.permissions import IsSuperUserPermission


class OrdersCrud(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        orders = Order.objects.prefetch_related("items__product").filter(
            user=request.user
        )

        try:
            serialized = OrderRetrieveSerializer(orders, many=True)
        except Exception as e:
            return Response(
                {"success": False, "message": "Error"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"success": True, "orders": serialized.data}, status=HTTP_200_OK
        )

    def create(self, request):
        serialized = OrderPlacement(data=request.data)
        if serialized.is_valid():
            order = Order.objects.create(user=request.user, totalBill=0)
            summation = 0
            for req in serialized.validated_data["requests"]:
                try:
                    product = Product.objects.get(product_id=req["product_id"])
                    summation += product.price * req["quantity"]
                    OrderItems.objects.create(
                        order=order, product=product, quantity=req["quantity"]
                    )
                except Product.DoesNotExist:
                    pass
            order.totalBill = summation
            order.save()
            return Response(
                {
                    "success": True,
                    "order_id": order.order_id,
                    "totalBill": order.totalBill,
                },
                status=HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "Bad Request"},
                status=HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            orders = Order.objects.prefetch_related("items__product").get(
                user=request.user, order_id=pk
            )
        except Order.DoesNotExist:
            return Response(
                {"success": False, "message": "Not Found"}, status=HTTP_404_NOT_FOUND
            )
        try:
            serialized = OrderRetrieveSerializer(orders)
        except Exception as e:
            return Response(
                {"success": False, "message": "Error"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response({"success": True, "order": serialized.data}, status=HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            order = Order.objects.get(order_id=pk)

        except Order.DoesNotExist:
            return Response(
                {"success": False, "message": "Not Found"}, status=HTTP_404_NOT_FOUND
            )

        serialized = OrderPlacement(data=request.data)
        if serialized.is_valid():
            summation = 0

            for req in serialized.validated_data["requests"]:
                if OrderItems.objects.filter(
                    order=order, product__id=req["product_id"]
                ).exists():
                    oldrecord = OrderItems.objects.select_related("product").get(
                        order=order, product__id=req["product_id"]
                    )

                    if oldrecord.quantity != req["quantity"]:
                        oldrecord.quantity = req["quantity"]
                        oldrecord.save()

                    summation += oldrecord.product.price * req["quantity"]

                else:
                    try:
                        product = Product.objects.get(product_id=req["product_id"])
                        summation += product.price * req["quantity"]
                        OrderItems.objects.create(
                            order=order, product=product, quantity=req["quantity"]
                        )
                    except Product.DoesNotExist:
                        pass

            order.totalBill = summation
            order.save()
            return Response(
                {
                    "success": True,
                    "order_id": order.order_id,
                    "totalBill": order.totalBill,
                },
                status=HTTP_200_OK,
            )

        else:
            return Response(
                {"success": False, "message": "Bad Request"},
                status=HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(order_id=pk)

        except Order.DoesNotExist:
            return Response(
                {"success": False, "message": "Not Found"}, status=HTTP_404_NOT_FOUND
            )

        OrderItems.objects.filter(order=order).delete()
        order.delete()

        return Response(
            {"success": True, "message": "Deleted"}, status=HTTP_204_NO_CONTENT
        )


class OrderAdminView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUserPermission]

    def get(self, request, *args, **kwargs):
        emails = request.GET.get("emails")
        if not emails:
            return Response(
                {"success": False, "message": "Send Emails in Param"},
                status=HTTP_400_BAD_REQUEST,
            )

        emails = emails.split(",")

        orders = (
            Order.objects.prefetch_related("items__product")
            .select_related("user")
            .filter(user__email__in=emails)
        )

        try:
            serialized = OrderRetrieveSerializerWithUserInfo(orders, many=True)
        except Exception as e:
            return Response(
                {"success": False, "message": "Error"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response = {}

        for ser in serialized.data:
            if ser["user"]["email"] not in response:
                response[ser["user"]["email"]] = [ser]
            else:
                response[ser["user"]["email"]].append(ser)
        return Response({"success": True, "orders": response})
