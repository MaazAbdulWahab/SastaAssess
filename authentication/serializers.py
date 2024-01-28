from rest_framework import serializers
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, instance):
        if User.objects.filter(email=instance["email"]).exists():
            raise serializers.ValidationError("Email Already Present")
        if User.objects.filter(username=instance["username"]).exists():
            raise serializers.ValidationError("Usernames Already Present")

        return instance

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
