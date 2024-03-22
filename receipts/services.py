import json

from django.core.paginator import Paginator

from .serializers import RecipeSerializer, RecipeCreateSerializer
from .models import Ingredient, RecipeIngredients, Recipe

def get_paginated_data(queryset, request):
    page_number = int(request.query_params.get('page', 1))
    page_limit = int(request.query_params.get('limit', 10))
    paginator = Paginator(queryset, page_limit)
    serializer = RecipeSerializer(paginator.page(page_number), 
                                many = True, 
                                context = {'request': request,
                                           'detail': False})
    data = {
        'data': serializer.data,
        'total': paginator.num_pages
    }
    return data

def _convert_ingredients_to_json(data):
    if isinstance(data, str):
        data = json.loads(data)
    if isinstance(data[0], str):
        data = json.loads(data[0])
    return data

def create_recipe(data):
    serializer = RecipeCreateSerializer(data = data)
    serializer.is_valid(raise_exception = True)
    recipe = Recipe.objects.create(**serializer.validated_data)
    return recipe

def create_recipe_ingredinets_relation(recipe, ingredients):
    result = []
    ingredients = _convert_ingredients_to_json(ingredients)
    for ingredient in ingredients:
        ingred = Ingredient.objects.get_or_create(ingredient_name = ingredient['ingredient_name'])
        amount = ingredient['amount']
        unit = ingredient['unit']
        relation = RecipeIngredients.objects.create(recipe = recipe,
                                                    ingredient = ingred[0],
                                                    amount = amount,
                                                    unit = unit)
        result.append(relation)
    return result