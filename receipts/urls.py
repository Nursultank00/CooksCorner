from django.urls import path

from .views import (
                    GetRecipeAPIView, 
                    AddRecipeAPIView,
                    RecipesByCategoryAPIView,
                    RecipesByChefAPIView,
                    SavedByUserRecipesAPIView,
                    LikeRecipeAPIView,
                    SaveRecipeAPIView,
                    SearchRecipesAPIView
)

urlpatterns = [
    path('', AddRecipeAPIView.as_view(), name = 'cookscorner-recipe-add'),
    path('detail/<slug:slug>/', GetRecipeAPIView.as_view(), name = 'cookscorner-recipe-detail'),
    path('by-category/', RecipesByCategoryAPIView.as_view(), name = 'cookscorner-recipes-by-categories'),
    path('by-chef/<slug:slug>/', RecipesByChefAPIView.as_view(), name = 'cookscorner-recipes-by-chef'),
    path('saved-recipes/', SavedByUserRecipesAPIView.as_view(), name = 'cookscorner-saved-recipes'),
    path('like/<slug:slug>/', LikeRecipeAPIView.as_view(), name = 'cookscorner-like-recipe'),
    path('save/<slug:slug>/', SaveRecipeAPIView.as_view(), name = 'cookscorner-save-recipe'),
    path('search/', SearchRecipesAPIView.as_view(), name = 'cookscorner-search-recipes'),
]