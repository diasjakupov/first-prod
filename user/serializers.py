from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from wall.serializers import BookSerializer

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
            'last_name',
            ]
        read_only_fields = ['date_joined',
                            ]

class PrivateUserSerializer(ModelSerializer):
    books_like=BookSerializer(many=True)
    class Meta:
        model = User
        fields=['id','username','first_name','date_joined','gender','image','books_like']
        read_only_fields = ['date_joined','books_like'
                            ]

