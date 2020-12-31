from rest_framework.serializers import ModelSerializer
from .models import User

class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'is_staff',
            'is_active',
            'password',
            'is_superuser',
            'user_permissions',
            'groups',
            'last_login',
            'email',
            'last_name'
            ]
        read_only_fields = ['date_joined',
                            ]

class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'is_staff',
            'is_active',
            'password',
            'is_superuser',
            'user_permissions',
            'groups',
            'last_login',
            ]
        read_only_fields = ['date_joined',
                            ]

