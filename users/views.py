from datetime import timedelta

from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import Response, APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from .serializers import SignupSerializer
from .models import ConfirmationCode, User
from .utils import EmailUtil
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
            status.HTTP_201_CREATED: "User has been created",
            status.HTTP_400_BAD_REQUEST: "Invalid data",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        token = RefreshToken().for_user(user).access_token
        token.set_exp(lifetime=timedelta(minutes=5))
        ConfirmationCode.objects.create(user = user, code = str(token))
        data = {'token':str(token),
                'to_email': user.email,
                'email_subject':'Verify your email'}
        EmailUtil.send_email(data)
        return Response({'email': serializer.data['email']}, status=status.HTTP_201_CREATED)
