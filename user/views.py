from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import generics, mixins
from .models import User
from .serializers import PublicUserSerializer,PrivateUserSerializer



class PublicUserViewset(ModelViewSet):
    queryset =  User.objects.all()
    serializer_class=PublicUserSerializer
    permission_classes=[permissions.AllowAny]

class PrivateUserViewSet(generics.RetrieveUpdateDestroyAPIView, mixins.CreateModelMixin):
    serializer_class=PrivateUserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.prefetch_related('books_like', 'books_like__types').get(id=self.request.user.id
        )

    def get_object(self):
        obj=self.get_queryset()
        return obj

    def post(self, request, *args, **kwargs):
        user=self.request.user
        user.image=request.data['image']
        user.save()
        serializer=PrivateUserSerializer(user)
        return Response(serializer.data)


        

    
    