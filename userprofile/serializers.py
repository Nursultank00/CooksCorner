from rest_framework import serializers
from autoslug.utils import slugify

from .models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    followers_num = serializers.SerializerMethodField()
    following_num = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'profile_picture', 'slug', 'followers_num', 'following_num']
        read_only_fields = ('followers_num', 'following_num')
        extra_kwargs = {'username': {"required": False},
                        'bio': {'required': False, 'allow_null': True},
                        'profile_picture': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

    def get_followers_num(self, obj):
        return len(obj.user.followers.all())
    
    def get_following_num(self, obj):
        return len(obj.following.all())