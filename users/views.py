import jwt

from decouple import config
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serializers import (
                          SignupSerializer,
                          LoginSerializer,
                          RefreshTokenSerializer,
                          ChangePasswordSerializer,
                          ChangePasswordForgotSerializer,
                          MailUrlSerializer
                         )
from .models import User, ConfirmationCode
from .users_services import (
                            create_token_and_send_to_email, 
                            get_user_by_token,
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
        data = request.data.copy()
        url = data.pop('url', config('EMAIL_LINK'))
        serializer = SignupSerializer(data = data)
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
            return Response({'Message': 'Invalid username.'}, status = status.HTTP_400_BAD_REQUEST)
        create_token_and_send_to_email(user = user, query = 'verify-account', url = url)
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
        operation_description = "Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "переотправить токен для "
                              "верификации почты. ",
        request_body = MailUrlSerializer,
        responses = {
            200: "The verification email has been sent. ",
            400: "User is already verified.",
        },
    )
    def post(self, request):
        user = request.user
        if user.is_verified:
            return Response({'Message':'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        url = data.pop('url', config('EMAIL_LINK'))
        create_token_and_send_to_email(user = user, query = 'verify-account', url = url)
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
        responses = {
            200: "Successfully logged in.",
            404: "User is not found.",
            404: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        data = {
            'email' : request.data['email'],
            'password' : request.data['password']
        }
        email = data['email']
        password = data['password']
        user = User.objects.filter(email = email).first()
        if user is None:
            return Response({'Error':'No user with this email.'}, status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'Error':'Wrong password!'}, status=status.HTTP_400_BAD_REQUEST)
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
            200: "Successfully logged out.",
            400: "Invalid token.",
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
        tags = ['Authorization'],
        operation_description = "Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "удалить собственный аккаунт. ",
        request_body = RefreshTokenSerializer,
        responses = {
            200: "User is successfully deleted.",
            400: "Invalid token.",
        },
    )
    def delete(self, request, *args, **kwargs):
        refresh_token = request.data['refresh']
        user = request.user
        try:
            destroy_token(refresh_token)
        except Exception:
            return Response({"Error": "Can't delete the user."}, status = status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({'Message': 'User has been successfully deleted.'}, status=status.HTTP_200_OK)

class ForgotPasswordAPIView(APIView):

    @swagger_auto_schema(
        tags = ['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "получить токен для сброса пароля. ",
        request_body = MailUrlSerializer,
        responses = {
            200: "Password is successfully changed.",
            400: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            user = User.objects.get(email = email)
        except Exception:
            return Response({"Error": "User is not found."}, status = status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        url = data.pop('url', config('EMAIL_LINK_PASSWORD'))
        create_token_and_send_to_email(user = user, query = 'change-password', url = url)
        return Response({'Message':'The verification email has been sent.'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность авторизованному пользователю "
                              "изменить пароль аккаунта. ",
        request_body = ChangePasswordSerializer,
        responses={
            200: "Password is successfully changed.",
            400: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data = request.data, context = {'user': user})
        serializer.is_valid(raise_exception = True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'Message': 'Password is changed successfully.'}, status=status.HTTP_200_OK)
    
class ForgotPasswordChangeAPIView(APIView):

    @swagger_auto_schema(
        tags=['Authorization'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "изменить пароль на новый. ",
        request_body = ChangePasswordForgotSerializer,
        responses={
            200: "Password is successfully changed.",
            400: "Invalid data.",
        },
    )
    def post(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            user = get_user_by_token(token)
        except jwt.exceptions.DecodeError:
            return Response({'Error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'Error':'Activation token expired'}, status=status.HTTP_400_BAD_REQUEST)
        password, password_confirm = request.data['password'], request.data['password_confirm']
        if password != password_confirm:
            return Response({'Error':"Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(password)
        except Exception as e:
            return Response({"Error": e}, status = status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({'Message': 'Password is changed successfully.'}, status=status.HTTP_200_OK)