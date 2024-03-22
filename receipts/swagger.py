from drf_yasg import openapi
from rest_framework import serializers

class IngredientsSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField()
    amount = serializers.CharField()
    unit = serializers.CharField()

    class Meta:
        abstract = True

class RecipeCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    meal_picture = serializers.ImageField()
    description = serializers.CharField()
    difficulty = serializers.CharField()
    preparation_time = serializers.IntegerField()
    ingredients = IngredientsSerializer(many = True)

    class Meta:
        abstract = True

class RecipeListSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.SlugField()
    meal_picture = serializers.ImageField()
    author_name = serializers.CharField()
    likes = serializers.IntegerField()
    saves = serializers.IntegerField()
    is_liked = serializers.BooleanField()
    is_saved = serializers.BooleanField()

    class Meta:
        abstract = True

class RecipeDetailSerializer(RecipeListSerializer):
    author_slug = serializers.SlugField()
    description = serializers.CharField()
    difficulty = serializers.CharField()
    preparation_time = serializers.IntegerField()
    ingredients = IngredientsSerializer(many = True)


recipe_detail_swagger = {
    'parameters': None,
    'request_body': None,
    'response': RecipeDetailSerializer
}

recipe_list_swagger = {
    'parameters': None,
    'request_body': None,
    'response': RecipeListSerializer
}

recipe_by_category_swagger = {
    'parameters': [
            openapi.Parameter('category', openapi.IN_QUERY, description = "Filter recipes by category. Default: Breakfast.", type = openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description = "Pagination page. Default: 1.", type = openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description = "Pagination limit. Default: 10.", type = openapi.TYPE_INTEGER),
    ],
    'request_body': None,
    'response': RecipeListSerializer
}

search_recipe_swagger = {
    'parameters': [
            openapi.Parameter('search', openapi.IN_QUERY, description = "Search recipes by name.", type = openapi.TYPE_STRING, required = True),
    ],
    'request_body': None,
    'response': RecipeListSerializer
}

add_recipe_swagger = {
    'parameters': None,
    'request_body': RecipeCreateSerializer,
    'response': None
}