from rest_framework.serializers import ModelSerializer, Serializer

class LoginSerializer(ModelSerializer):
    class Meta:
        fields = ['email']

