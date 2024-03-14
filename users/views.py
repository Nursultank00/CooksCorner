import jwt

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import Response, APIView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
                          SignupSerializer,
                          LoginSerializer,
                         )
from .models import User, ConfirmationCode
from .users_services import (
                            create_token_and_send_to_email, 
                            get_user_by_token,
                            validate_user,
                            get_tokens_for_user
                            )
# Create your views here.

class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer
    @swagger_auto_schema(
        tags=['Registration'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "обновить токен доступа (Access Token) "
                              "с помощью токена обновления (Refresh Token). "
                              "Токен обновления позволяет пользователям "
                              "продлить срок действия своего Access Token без "
                              "необходимости повторной аутентификации.",
        request_body=SignupSerializer,                      
        responses={
            status.HTTP_201_CREATED: "User has been created.",
            status.HTTP_400_BAD_REQUEST: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            serializer.save()
        except Exception as e:
            Response(e, status=status.HTTP_400_BAD_REQUEST)
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        create_token_and_send_to_email(user = user, method = "signup")
        return Response({"Message": "User has been created and confirmation email has been sent."}, status=status.HTTP_201_CREATED)

class VerifyEmailAPIView(APIView):
    @swagger_auto_schema(
        tags=['Registration'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "верифицироваться "
                              "с помощью отправленного на почту токена.",
        manual_parameters=[
            openapi.Parameter('Token', in_=openapi.IN_QUERY,
                             description="Уникальный токен для верификации почты.",
                             type=openapi.TYPE_STRING)
        ],
        responses={
            status.HTTP_200_OK: "Successfully verified.",
            status.HTTP_400_BAD_REQUEST: "Invalid data.",
        }
    )
    def get(self, request):
        token = request.GET.get('token')
        try:
            user = get_user_by_token(token)
        except jwt.exceptions.DecodeError:
            return Response({'Error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'Error':'Activation token expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_verified:
            return Response({'Message':'User is already verified'}, status=status.HTTP_200_OK)
        user_code = ConfirmationCode.objects.get(user = user)
        if token != user_code.code:
            return Response({'Message':'Activation token expired'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()
        return Response({'Message':'User is successfuly verified'}, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    @swagger_auto_schema(
        tags=['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "авторизоваться с помощью логина и пароля."
                              "Возвращает токен доступа (Access Token) "
                              "и токен обновления (Refresh Token). ",
        request_body = LoginSerializer,
        responses={
            status.HTTP_200_OK: "Successfully logged in.",
            status.HTTP_404_NOT_FOUND: "User is not found",
            status.HTTP_400_BAD_REQUEST: "Invalid data",
        },
    )
    def post(self, request, *args, **kwargs):
        data = {
            'email' : request.data['email'],
            'password' : request.data['password']
        }
        user = validate_user(data)
        tokens = get_tokens_for_user(user)
        return Response(tokens, status = status.HTTP_200_OK)

class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "обновить токен доступа (Access Token) "
                              "с помощью токена обновления (Refresh Token). "
                              "Токен обновления позволяет пользователям "
                              "продлить срок действия своего Access Token без "
                              "необходимости повторной аутентификации.",
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)