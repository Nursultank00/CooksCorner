from django.urls import path

from .views import (
                    GetRecipeAPIView, 
                    AddRecipeAPIView,
                    RecipesByCategoryAPIView
)

urlpatterns = [
    path('', AddRecipeAPIView.as_view(), name = 'Recipe-add'),
    path('detail/<slug:slug>/', GetRecipeAPIView.as_view(), name = 'Recipe-detail'),
    path('by-category/', RecipesByCategoryAPIView.as_view(), name = 'Recipe-by-categories')
]