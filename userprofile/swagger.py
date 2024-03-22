from drf_yasg import openapi
from rest_framework import serializers

class MyProfileRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    bio = serializers.CharField()
    profile_picture = serializers.ImageField()

    class Meta:
        abstract = True

class ProfileDetailSerializer(MyProfileRequestSerializer):
    slug = serializers.SlugField()
    followers = serializers.IntegerField()
    following = serializers.IntegerField()
    is_followed = serializers.BooleanField()
    recipes = serializers.IntegerField()

class MyProfileResponseSerializer(ProfileDetailSerializer):
    is_verified = serializers.BooleanField()

class ProfileListSerializer(serializers.Serializer):
    username = serializers.CharField()
    profile_picture = serializers.ImageField()
    slug = serializers.SlugField()

    class Meta:
        abstract = True

user_detail_swagger = {
    'parameters': None,
    'request_body': None,
    'response': ProfileDetailSerializer
}

myprofile_swagger = {
    'parameters': None,
    'request_body': MyProfileRequestSerializer,
    'response': MyProfileResponseSerializer
}

search_user_swagger = {
    'parameters': [
            openapi.Parameter('search', openapi.IN_QUERY, description = "Search users by usernames.", type = openapi.TYPE_STRING, required = True),
    ],
    'request_body': None,
    'response': ProfileListSerializer
}