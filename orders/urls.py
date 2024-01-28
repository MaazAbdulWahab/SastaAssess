from orders.views import OrdersCrud, OrderAdminView
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register("order", OrdersCrud, basename="user")
urlpatterns = router.urls

urlpatterns.append(path("ordersfetch", OrderAdminView.as_view()))
