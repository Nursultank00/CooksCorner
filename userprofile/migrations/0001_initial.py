# Generated by Django 4.2.5 on 2024-03-20 12:42

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='cookscorner/user_profile')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='username', unique=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='userprofile.userprofile')),
            ],
        ),
    ]
