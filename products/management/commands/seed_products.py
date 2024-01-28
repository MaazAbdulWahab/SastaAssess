from products.models import Product

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = [
            {"name": "Biscuit", "price": 10},
            {"name": "Candy", "price": 2},
            {"name": "Bread", "price": 80},
            {"name": "Ice Cream", "price": 150},
        ]

        for pr in products:
            Product.objects.create(name=pr["name"], price=pr["price"])
