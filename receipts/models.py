from django.db import models

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
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=10, choices = CATEGORY_CHOICES, default = 'Lunch')

    def __str__(self):
        return self.category_name
    

class Receipt(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name = 'author', related_name = 'receipts', on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices = DIFFICULTY_CHOICES, default = 'Medium')
    meal_picture = models.ImageField(upload_to = 'cookscorner/receipt_images')
    preparation_time = models.PositiveIntegerField(default = 30)
    liked_by = models.ManyToManyField(UserProfile, related_name='likes')
    saved_by = models.ManyToManyField(UserProfile, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length = 30)
    amount = models.CharField(max_length = 40)
    receipt = models.ForeignKey(Receipt, verbose_name = 'receipt', related_name = 'ingredients', on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.ingredient_name}:{self.receipt}"