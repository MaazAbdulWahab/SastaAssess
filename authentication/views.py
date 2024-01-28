from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from authentication.serializers import *
from rest_framework.authentication import TokenAuthentication

# Create your views here.


class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data["email"])

                if user.check_password(serializer.validated_data["password"]):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        {"success": True, "token": token.key}, status=HTTP_200_OK
                    )

                else:
                    return Response(
                        {"success": False, "message": "Wrong Password"},
                        status=HTTP_400_BAD_REQUEST,
                    )

            except User.DoesNotExist:
                return Response(
                    {"success": False, "message": "User Not Found"},
                    status=HTTP_404_NOT_FOUND,
                )

        else:
            return Response(
                {"success": False, "message": "Bad Request"},
                status=HTTP_400_BAD_REQUEST,
            )


class Register(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=HTTP_200_OK)
        else:
            return Response(
                {"success": False, "message": "Bad Request"},
                status=HTTP_400_BAD_REQUEST,
            )


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "message": "Successfull"}, status=HTTP_200_OK)
