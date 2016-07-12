from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CybPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        print(repr(self.page))
        return Response(OrderedDict([
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('per_page', self.page.paginator.per_page),
            ('total', self.page.paginator.count),
            ('results', data)
        ]))
