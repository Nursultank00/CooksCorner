from django.db import models
from autoslug import AutoSlugField

from userprofile.models import UserProfile

CATEGORY_CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
)

DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
)
    
class Recipe(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name = 'author', related_name = 'recipes', on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices = DIFFICULTY_CHOICES, default = 'Medium')
    meal_picture = models.ImageField(upload_to = 'cookscorner/recipe_images', max_length = 500)
    preparation_time = models.PositiveIntegerField(default = 30)
    category = models.CharField(max_length=10, choices = CATEGORY_CHOICES, default = 'Lunch')
    slug = AutoSlugField(populate_from = 'name', unique = True, always_update=True)
    liked_by = models.ManyToManyField(UserProfile, related_name='likes', blank=True)
    saved_by = models.ManyToManyField(UserProfile, related_name='saves', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}; slug: {self.slug}"

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return f"{self.ingredient_name}"
    

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name = 'recipe', related_name = 'ingredients', on_delete = models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, verbose_name = 'ingredient', related_name = 'recipe', on_delete = models.CASCADE)
    amount = models.CharField(max_length = 40)
    unit = models.CharField(max_length = 40)

    def __str__(self):
        return f"{self.recipe.name}:{self.recipe.slug}:{self.ingredient.ingredient_name}"