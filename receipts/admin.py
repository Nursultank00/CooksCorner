from django.contrib import admin

from .models import Receipt, Ingredient, Category
# Register your models here.

admin.site.register(Receipt)
admin.site.register(Category)
admin.site.register(Ingredient)
