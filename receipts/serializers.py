from rest_framework import serializers

from .models import Recipe, Ingredient

class IngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'amount', 'recipe']
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'amount', 'unit']

class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['author', 'name', 'description', 'difficulty', 'meal_picture',
                  'preparation_time', 'category']
class AddRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many = True)
    class Meta:
        model = Recipe
        fields = ['author', 'name', 'description', 'difficulty', 'ingredients', 'meal_picture',
                  'preparation_time', 'category']
        
class RecipeSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author_slug = serializers.ReadOnlyField(source='author.slug')
    ingredients = IngredientSerializer(many = True)
    class Meta:
        model = Recipe
        fields = ['author_name', 'author_slug', 'name', 'description', 'difficulty', 'slug', 
                  'meal_picture', 'preparation_time', 'ingredients']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        representation['likes'] = instance.liked_by.count()
        representation['saves'] = instance.saved_by.count()
        representation['is_liked'] = instance.liked_by.filter(user = user).exists()
        representation['is_saved'] = instance.saved_by.filter(user = user).exists()
        if not self.context['detail']:
            representation.pop('description')
            representation.pop('difficulty')
            representation.pop('preparation_time')
            representation.pop('ingredients')
            representation.pop('author_slug')
        return representation