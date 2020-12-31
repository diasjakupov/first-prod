from django.contrib import admin
from .models import Book, Page, Chapter, Types, Genre, Category

admin.site.register(Book)
admin.site.register(Page)
admin.site.register(Chapter)
admin.site.register(Types)
admin.site.register(Genre)
admin.site.register(Category)