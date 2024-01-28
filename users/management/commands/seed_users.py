from django.contrib.auth.models import User

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = [
            {
                "username": "adminuser",
                "email": "adminuser@gmail.com",
                "password": "adminuserpasswordprotected",
                "is_superuser": True,
                "is_staff": True,
            },
            {
                "username": "usera",
                "email": "usera@gmail.com",
                "password": "userapasswordprotected",
            },
            {
                "username": "userb",
                "email": "userb@gmail.com",
                "password": "userbpasswordprotected",
            },
        ]

        for us in users:
            user = User.objects.create(
                username=us["username"],
                email=us["email"],
                is_superuser=us.get("is_superuser", False),
                is_staff=us.get("is_staff", False),
            )
            user.set_password(us["password"])
            user.save()
