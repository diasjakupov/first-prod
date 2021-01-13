from django.contrib import admin
from .models import Book, Page, Chapter, Types, Genre, Category, Rating, RatingStars

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    search_fields=['title', 'book__title']
    model = Chapter
    list_display=['title', 'id']
    list_per_page=25 

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields=['chapter__title']
    model = Page
    list_display=['__str__', 'id']
    list_per_page=15

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields=['title']
    model = Book
    fields=['title','description','category','genre','types','views', 'status', 'poster', 'average_rating']
    list_display=['title', 'id'] 
    list_per_page=25  


admin.site.register(Types)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(RatingStars)