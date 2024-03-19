# Generated by Django 4.2.5 on 2024-03-19 00:08

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0002_alter_userprofile_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Medium', max_length=10)),
                ('meal_picture', models.ImageField(null=True, upload_to='cookscorner/recipe_images')),
                ('preparation_time', models.PositiveIntegerField(default=30)),
                ('category', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], default='Lunch', max_length=10)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='userprofile.userprofile', verbose_name='author')),
                ('liked_by', models.ManyToManyField(blank=True, null=True, related_name='likes', to='userprofile.userprofile')),
                ('saved_by', models.ManyToManyField(blank=True, null=True, related_name='saves', to='userprofile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=30)),
                ('amount', models.CharField(max_length=40)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='receipts.recipe', verbose_name='recipe')),
            ],
        ),
    ]
