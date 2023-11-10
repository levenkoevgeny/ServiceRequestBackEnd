from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password',
                  'avatar', 'phone_number',
                  'is_superuser',
                  'is_staff',
                  'first_name',
                  'last_name',
                  'is_active',
                  'date_joined',
                  'last_login',
                  'can_be_executor'
                  ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)