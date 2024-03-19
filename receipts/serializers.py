from rest_framework import serializers

from .models import Recipe, Ingredient

class RecipeSerializer(serializers.ModelSerializer):
    likes_num = serializers.SerializerMethodField()
    saves_num = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    author_name= serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Recipe
        fields = ['author_name', 'name', 'description', 'difficulty', 'slug', 
                  'meal_picture', 'preparation_time', 'likes_num', 'saves_num',
                  'is_liked', 'is_saved']
        # read_only_fields = ('author_name', 'likes_num', 'saves_num', 'slug',
        #                     'is_liked', 'is_saved')
        # extra_kwargs = {'name': {"required": False},
        #                 'description': {'required': False, 'allow_null': True},
        #                 'difficulty': {'required': False},
        #                 'meal_picture': {'required': False},
        #                 'preparation_time': {'required': False},
        # }
    
    def get_likes_num(self, obj):
        return len(obj.liked_by.all())
    
    def get_saves_num(self, obj):
        return len(obj.liked_by.all())
    
    def get_is_liked(self, obj):
        user =  self.context['request'].user
        return obj.liked_by.filter(user = user).exists()

    def get_is_saved(self, obj):
        user =  self.context['request'].user
        return obj.saved_by.filter(user = user).exists()

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'amount']
class AddRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many = True)
    class Meta:
        model = Recipe
        fields = ['author', 'name', 'description', 'difficulty', 'ingredients',
                  'preparation_time', 'category']
        
class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['author', 'name', 'description', 'difficulty',
                  'preparation_time', 'category']
        
class IngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'amount', 'recipe']


