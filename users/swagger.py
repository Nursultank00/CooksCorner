from drf_yasg import openapi
from rest_framework import serializers

class ResendEmailSerializer(serializers.Serializer):
    url = serializers.URLField()

    class Meta:
        abstract = True

class ForgotPasswordSerializer(ResendEmailSerializer):
    email = serializers.EmailField()

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        abstract = True

class SignupRequestSerializer(LoginRequestSerializer):
    username = serializers.CharField()
    password_confirm = serializers.CharField()
    url = serializers.URLField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    class Meta:
        abstract = True

class TokenResponseSerializer(RefreshTokenSerializer):
    access = serializers.CharField()

class ForgotPasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    class Meta:
        abstract = True

signup_swagger = {
    'parameters': None,
    'request_body': SignupRequestSerializer,
    'response': TokenResponseSerializer
}

login_swagger = {
    'parameters': None,
    'request_body': LoginRequestSerializer,
    'response': TokenResponseSerializer
}

resend_swagger = {
    'parameters': None,
    'request_body': ResendEmailSerializer,
    'response': None
}

logout_swagger = {
    'parameters': None,
    'request_body': RefreshTokenSerializer,
    'response': None
}

forgot_password_swagger = {
    'parameters': None,
    'request_body': ForgotPasswordSerializer,
    'response': None
}

forgot_password_change_swagger = {
    'parameters': [
            openapi.Parameter('token', openapi.IN_QUERY, description = "Token that has been sent to email for password change.", type = openapi.TYPE_STRING),
    ],
    'request_body': ForgotPasswordChangeSerializer,
    'response': None
}