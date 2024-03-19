from rest_framework.views import Response, status, APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema

from .models import Recipe
from .services import get_paginated_data
from .serializers import (
                        RecipeSerializer, 
                        AddRecipeSerializer, 
                        IngredientSerializer, 
                        RecipeCreateSerializer
)
from userprofile.models import UserProfile

# Create your views here.
class GetRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "подробную информацию "
                              "о рецепте.",                    
        responses = {
            200: RecipeSerializer,
            404: "Recipe is not found.",
        },
    )
    def get(self, request, slug, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(slug = slug)
        except Exception:
            return Response({"Error": "Recipe is not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность создать "
                              "новый рецепт.",
        request_body = AddRecipeSerializer,                   
        responses = {
            201: "Recipe is created.",
            400: "Invalid data.",
            403: "User is not verified."
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_verified:
            return Response({"Error": "User is not verified."}, status = status.HTTP_403_FORBIDDEN)
        data = request.data
        data['author'] = request.user.profile.id
        try:
            ingredients = data.pop('ingredients')
        except Exception:
            return Response({"Ingredients": "Required field"}, status=status.HTTP_400_BAD_REQUEST)
        ingred_serializer = IngredientSerializer(data = ingredients, many = True)
        ingred_serializer.is_valid(raise_exception = True)
        serializer = RecipeCreateSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        recipe = serializer.save()
        for item in ingred_serializer.validated_data:
            item['recipe'] = recipe
        ingred_serializer.save()
        return Response({"Message": "Recipe is created."}, status=status.HTTP_201_CREATED)

class RecipesByCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "все рецепты определенной категории. ",            
        responses = {
            200: RecipeSerializer
        },
    )
    def get(self, request, format=None):
        category = request.query_params.get('category', 'Breakfast')
        queryset = Recipe.objects.filter(category = category)
        data = get_paginated_data(queryset, request)
        return Response(data, status = status.HTTP_200_OK)
    

class RecipesByChefAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "все рецепты определенного пользователя. ",                  
        responses = {
            200: RecipeSerializer,
            404: "User profile is not found.",
        },
    )
    def get(self, request, slug, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Recipe.objects.filter(author = profile)
        data = get_paginated_data(queryset, request)
        return Response(data, status = status.HTTP_200_OK)
    
class SavedByUserRecipesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "все сохраненные пользователем рецепты. ",              
        responses = {
            200: RecipeSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        queryset = profile.saves.all()
        data = get_paginated_data(queryset, request)
        return Response(data, status = status.HTTP_200_OK)
    

class SaveRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "все сохраненные пользователем рецепты. ",                 
        responses = {
            200: "Success.",
            403: "User is not verified.",
            404: "Recipe is not found."
        },
    )
    def put(self, request, slug, *args, **kwargs):
        user = request.user
        if not user.is_verified:
            return Response({"Error": "User is not verified."}, status = status.HTTP_403_FORBIDDEN)
        profile = user.profile
        try:
            recipe = Recipe.objects.get(slug = slug)
        except Exception:
            return Response({"Error": "Recipe is not found."}, status = status.HTTP_404_NOT_FOUND)
        if profile in recipe.saved_by.all():
            recipe.saved_by.remove(profile)
        else:
            recipe.saved_by.add(profile)
        return Response({"Error": "Success."}, status = status.HTTP_200_OK)

class LikeRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность сохранить рецепт. ",                
        responses = {
            200: "Success.",
            403: "User is not verified.",
            404: "Recipe is not found."
        },
    )
    def put(self, request, slug, *args, **kwargs):
        user = request.user
        if not user.is_verified:
            return Response({"Error": "User is not verified."}, status = status.HTTP_403_FORBIDDEN)
        profile = user.profile
        try:
            recipe = Recipe.objects.get(slug = slug)
        except Exception:
            return Response({"Error": "Recipe is not found."}, status = status.HTTP_404_NOT_FOUND)
        if profile in recipe.liked_by.all():
            recipe.liked_by.remove(profile)
        else:
            recipe.liked_by.add(profile)
        return Response({"Error": "Success."}, status = status.HTTP_200_OK)
    
class SearchRecipesAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность найти рецепт по названию. ",                
        responses = {
            200: RecipeSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        queryset = Recipe.objects.all()
        queryset = self.filter_queryset(queryset)
        data = get_paginated_data(queryset, request)
        return Response(data, status = status.HTTP_200_OK)