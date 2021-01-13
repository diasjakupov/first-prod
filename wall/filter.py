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
    average_rating=django_filters.NumberFilter(field_name='average_rating', method='order_average_rating')

    class Meta:
        model = Book
        fields=['category','types','genre']

    def order_views(self, queryset, name, value):
        return queryset.order_by('-views')[:8]

    def title_filter(self, queryset, name, value):
        print(value)
        return queryset.filter(title__contains=value)

    def order_average_rating(self, queryset, name, value):
        return queryset.order_by('-average_rating')[:12]


    