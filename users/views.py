import jwt

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
                          SignupSerializer,
                          LoginSerializer,
                          RefreshTokenSerializer,
                          MailSerializer,
                         )
from .models import User, ConfirmationCode
from .users_services import (
                            create_token_and_send_to_email, 
                            get_user_by_token,
                            validate_user,
                            get_tokens_for_user,
                            destroy_token,
                            )
from userprofile.models import UserProfile
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
            201: "User has been created.",
            400: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            serializer.save()
        except Exception as e:
            Response(e, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email = serializer.validated_data['email'])
        try:
            UserProfile.objects.create(user = user, username = serializer.validated_data['username'])
        except Exception as e:
            user.delete()
            raise e
            return Response({'Message': 'Invalid username.'}, status = status.HTTP_400_BAD_REQUEST)
        create_token_and_send_to_email(user = user)
        tokens = get_tokens_for_user(user)
        return Response(tokens, status = status.HTTP_201_CREATED)
        
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
            200: "Successfully verified.",
            400: "Invalid token.",
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
            return Response({'Error':'Activation token expired'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()
        return Response({'Message':'User is successfuly verified'}, status=status.HTTP_200_OK)

class SendVerifyEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Registration'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "переотправить токен для "
                              "верификации почты. ",
        responses= {
            status.HTTP_200_OK: "Successfully verified.",
            status.HTTP_404_NOT_FOUND: "User is not found.",
        },
    )
    def post(self, request):
        user = request.user
        user = User.objects.get(email=user.email)
        if user.is_verified:
            return Response({'Message':'User is already verified.'}, status=status.HTTP_200_OK)
        create_token_and_send_to_email(user = user)
        return Response({'Message':'The verification email has been sent.'}, status=status.HTTP_200_OK)

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
            status.HTTP_404_NOT_FOUND: "User is not found.",
            status.HTTP_400_BAD_REQUEST: "Invalid data.",
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
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "разлогиниться из приложения "
                              "с помощью токена обновления (Refresh Token). ",
        request_body = RefreshTokenSerializer,
        responses={
            status.HTTP_200_OK: "Successfully logged out.",
            status.HTTP_400_BAD_REQUEST: "Invalid token.",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            destroy_token(refresh_token)
            return Response({"Message": "You have successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"Error": "Unable to log out."}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "удалить собственный аккаунт. ",
        request_body = RefreshTokenSerializer,
        responses={
            status.HTTP_200_OK: "User is successfully deleted.",
            status.HTTP_400_BAD_REQUEST: "Invalid token.",
        },
    )
    def delete(self, request, *args, **kwargs):
        refresh_token = request.data['refresh']
        user = request.user
        try:
            destroy_token(refresh_token)
        except Exception:
            return Response({"Error": "Can't delete the user."}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({'Message': 'User has been successfully deleted.'}, status=status.HTTP_200_OK)