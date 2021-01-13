from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, pagination
from .models import Book, Page, Chapter, Rating, RatingStars
from django.contrib.auth import get_user_model


class BookSerializer(ModelSerializer):
    types=serializers.StringRelatedField()
    class Meta:
        model = Book
        fields=['id','title','types','views','poster']

class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields=['picture',]

class ChapterSerializer(ModelSerializer):
    book=BookSerializer()
    class Meta:
        model = Chapter
        fields=['id','book','title', 'created_date']

class ChapterDetailSerializer(ModelSerializer):
    page=PageSerializer(many=True)
    class Meta:
        model = Chapter
        fields=['title', 'created_date','page']


class TypeGenreCatSerializer(serializers.Serializer):
    title=serializers.CharField()



class DetailBookSerializer(ModelSerializer):
    category=serializers.StringRelatedField(many=True)
    genre=serializers.StringRelatedField(many=True)
    types=serializers.StringRelatedField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields=[
        'id',
        'title', 'description', 
        'views','created_date',
        'status','category',
        'genre','types',
        'average_rating','poster',
        "is_liked"
        ]

    def get_is_liked(self, obj):
        request = self.context['request']
        try:
            users_id = [i.id for i in obj.likes.all()]
            if request.user.id in users_id:
                return True
        except BaseException:
            return False

class UserForReviewSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields=['username', 'image','id']


class RatingSerializer(ModelSerializer):
    user=UserForReviewSerializer()
    star=serializers.StringRelatedField()
    class Meta:
        model = Rating
        fields = ['user', 'book', 'star','text']

class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'book', 'star','text']

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
            book=validated_data.get('book'),
            user=validated_data.get('user'),
            defaults={'star': validated_data.get('star'), 'text':validated_data.get('text')}
        )
        return rating