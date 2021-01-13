from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict

class ChapterPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_count', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
         ]))

class BookPagination(pagination.PageNumberPagination):
    page_size = 15


    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_count', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
         ]))

