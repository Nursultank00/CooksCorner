from uuid import uuid4

from django.db import models
from autoslug import AutoSlugField

from users.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name = 'user', related_name = 'profile', on_delete = models.CASCADE)
    username = models.CharField(max_length = 255)
    bio = models.TextField(blank = True, null = True)
    profile_picture = models.ImageField(upload_to = 'cookscorner/user_profile', blank = True, null = True)
    following = models.ManyToManyField('self', symmetrical = False, related_name = 'followers', blank = True)
    slug = AutoSlugField(populate_from = 'username', unique = True, always_update=True)

    def __str__(self):
        return f"Username: {self.username}; Email: {self.user}; Slug: {self.slug}"