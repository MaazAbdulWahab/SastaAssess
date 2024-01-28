from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import *
from utils.permissions import *
from django.contrib.auth.models import User

# Create your views here.


class Me(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "success": True,
                "username": request.user.username,
                "email": request.user.email,
            },
            status=HTTP_200_OK,
        )


class AllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUserPermission]

    def get(self, request):
        users = list(
            User.objects.filter(is_superuser=False).values("email", "username")
        )

        return Response({"success": True, "users": users}, status=HTTP_200_OK)
