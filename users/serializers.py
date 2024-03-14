from rest_framework import serializers

from .models import User

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=15, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=15, min_length=8, write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)