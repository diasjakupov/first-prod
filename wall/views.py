from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Book, Chapter, Page
from .serializers import BookSerializer, DetailBookSerializer
from django.db.models import F

class BookViewSet(ModelViewSet):
    queryset=Book.objects.all()
    serializer_class=BookSerializer

    def retrieve(self, request, pk):
        book=Book.objects.filter(pk=pk).prefetch_related('chapter', 'category','genre','types')
        book.update(views=F('views')+1)
        serializer=DetailBookSerializer(book[0])
        return Response(serializer.data)


        
