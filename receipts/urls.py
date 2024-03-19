from django.urls import path

from .views import (
                    GetRecipeAPIView, 
                    AddRecipeAPIView,
                    RecipesByCategoryAPIView,
                    RecipesByChefAPIView
)

urlpatterns = [
    path('', AddRecipeAPIView.as_view(), name = 'Recipe-add'),
    path('detail/<slug:slug>/', GetRecipeAPIView.as_view(), name = 'recipe-detail'),
    path('by-category/', RecipesByCategoryAPIView.as_view(), name = 'recipes-by-categories'),
    path('by-chef/<slug:slug>/', RecipesByChefAPIView.as_view(), name = 'recipes-by-chef')
]