from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import PublicUserSerializer,PrivateUserSerializer


class PublicUserViewset(ModelViewSet):
    queryset =  User.objects.all()
    serializer_class=PublicUserSerializer

class PrivateUserViewSet(ModelViewSet):
    serializer_class=PrivateUserSerializer
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    