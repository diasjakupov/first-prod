from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Book, Page, Chapter

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields=['title','description','views''poster',]

class ChapterSerializer(ModelSerializer):
    class Meta:
        model = Chapter
        fields=['title', 'created_date']


class DetailBookSerializer(ModelSerializer):
    chapter=ChapterSerializer(many=True)
    category=serializers.StringRelatedField(many=True)
    genre=serializers.StringRelatedField(many=True)
    types=serializers.StringRelatedField()
    class Meta:
        model = Book
        fields=[
        'title', 'description', 
        'views','created_date',
        'status','category',
        'genre','types',
        'poster','chapter'
        ]