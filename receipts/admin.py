from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredients
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredients)
