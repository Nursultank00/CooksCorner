from django.core.paginator import Paginator

from .serializers import RecipeSerializer

def get_paginated_data(queryset, request):
    page_number = int(request.query_params.get('page', 1))
    page_limit = int(request.query_params.get('limit', 10))
    paginator = Paginator(queryset, page_limit)
    serializer = RecipeSerializer(paginator.page(page_number), 
                                many = True, 
                                context = {'request': request})
    data = {
        'data': serializer.data,
        'total': paginator.num_pages
    }
    return data