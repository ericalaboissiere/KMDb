from rest_framework import serializers
from django.contrib.auth.models import User
import ipdb


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'is_superuser', 'username',
                  'first_name', 'last_name', 'password', 'id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CredentialSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
