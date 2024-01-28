from django.urls import path
from products.views import *

urlpatterns = [
    path("all/", ProductList.as_view()),
]
