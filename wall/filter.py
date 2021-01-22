import django_filters
from .models import Book, Category, Types, Genre


class FilterIn(django_filters.BaseInFilter, django_filters.CharFilter):
    pass



class BookFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(field_name='title', method='title_filter')
    category=FilterIn('category__title', lookup_expr='in', distinct=True)
    types=FilterIn('types__title', lookup_expr='in')
    genre=FilterIn('genre__title', lookup_expr='in', distinct=True)
    views=django_filters.NumberFilter(field_name='views', method='order_views')
    average_rating=django_filters.NumberFilter(field_name='average_rating', method='random_order')

    class Meta:
        model = Book
        fields=['category','types','genre']

    def order_views(self, queryset, name, value):
        return queryset.order_by('-views')[:8]

    def title_filter(self, queryset, name, value):
        return queryset.filter(title__contains=value)

    def random_order(self, queryset, name, value):
        return queryset.order_by('?')[:15]

# class ChapterFilter(django_filters.FilterSet):
#     order_by_created_date=django_filters.NumberFilter(field_name='views', method='created_date')

#     def created_date(self, queryset, name, value):
#         return queryset.order_by("-created_date")


    