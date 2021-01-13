from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
import os
from .models import Book, Chapter, Page, Rating, Types, Genre, Category, Rating
from .serializers import (BookSerializer, 
DetailBookSerializer, 
CreateRatingSerializer, 
PageSerializer,
ChapterDetailSerializer,
ChapterSerializer,
TypeGenreCatSerializer,RatingSerializer)
from .filter import BookFilter
from .paginations import ChapterPagination, BookPagination 

from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

class BookViewSet(ModelViewSet):
    """
    Список книг с пагинацией
    """
    queryset=Book.objects.all().prefetch_related('category','genre','types').order_by('-id')
    serializer_class=BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    pagination_class=BookPagination

    permission_classes_by_action={'retrieve': [AllowAny], "update": [IsAuthenticated]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            return [permission() for permission in self.permission_classes]

    def retrieve(self, request, pk):
        book=Book.objects.prefetch_related('chapter', 'category','genre','types', 'rating', 'rating__star').get(pk=pk)
        serializer=DetailBookSerializer(book)
        return Response(serializer.data)


    def update(self, request, pk):
        data=request.data
        if data['likes_update']:
            book=get_object_or_404(Book, pk=data['book'])
            if book.likes.filter(id=request.user).exists():
                book.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return self.retrieve(request, pk)
        return super().update(request, pk)

class DetailBookview(generics.RetrieveUpdateAPIView):
    queryset=Book.objects.prefetch_related('chapter', 'category','genre','types', 'rating', 'rating__star', 'likes').all()
    serializer_class=DetailBookSerializer

    def retrieve(self, request, pk):
        book=Book.objects.filter(pk=pk).prefetch_related('chapter', 'category','genre','types', 'rating', 'rating__star')
        book.update(views=F('views')+1)
        return super().retrieve(request, pk)

    def update(self, request, pk):
        data=request.data
        if data['likes_update']:
            book=get_object_or_404(Book, pk=pk)
            if book.likes.filter(id=request.user.id).exists():
                book.likes.remove(request.user)
            else:
                book.likes.add(request.user)
        return Response(DetailBookSerializer(book, context={'request': request}).data)

class CreateRatingView(generics.CreateAPIView):
    """
    Добавление рейтинга
    """
    serializer_class = CreateRatingSerializer
    queryset = Rating.objects.all().prefetch_related('star','book','user')
    permission_classes=[permissions.IsAuthenticated]

class PageViewSet(ModelViewSet):
    """
    Лист страниц определенной главы
    """
    serializer_class = ChapterDetailSerializer
    queryset=Chapter.objects.all().prefetch_related('page')

class ChapterList(generics.ListAPIView):
    """
    Список глав определенной книги
    """
    serializer_class = ChapterSerializer
    pagination_class=ChapterPagination

    def get_queryset(self):
        return Chapter.objects.filter(book_id=self.kwargs['pk']).order_by('-created_date')

class AllListChapters(ModelViewSet):
    """
    Список глав
    """
    queryset=Chapter.objects.order_by('-created_date').prefetch_related('book')[:8]
    serializer_class=ChapterSerializer

class TypesList(generics.ListAPIView):
    queryset=Types.objects.all()
    serializer_class=TypeGenreCatSerializer
    
class GenreList(generics.ListAPIView): 
    queryset=Genre.objects.all()
    serializer_class=TypeGenreCatSerializer

class CategoryList(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=TypeGenreCatSerializer

class BookList(generics.ListAPIView):
    """
    Список книг без пагинации
    """
    queryset=Book.objects.all().prefetch_related('category','genre','types')
    serializer_class=BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

class getReviewsById(generics.ListAPIView):
    serializer_class=RatingSerializer

    def get_queryset(self):
        rating=Rating.objects.filter(book_id=self.kwargs['pk']).select_related('star','book','user')
        return rating