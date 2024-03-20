from rest_framework import serializers

from .models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'profile_picture', 'slug']
        read_only_fields = ('slug',)
        extra_kwargs = {
                        'bio': {'required': False, 'allow_null': True},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['detail']:
            representation['followers'] = instance.followers.count()
            representation['following'] = instance.following.count()
        else:
            representation.pop('bio')
        return representation