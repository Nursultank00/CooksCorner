from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import Response, APIView
from drf_yasg.utils import swagger_auto_schema

from .serializers import SignupSerializer
from .models import User
from .users_services import create_token_and_send_to_email
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
            Response(e, status=status.HTTP_400_BAD_REQUEST)
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        create_token_and_send_to_email(user = user, method = "signup")
        return Response({"Message": "User has been created and confirmation email has been sent."}, status=status.HTTP_201_CREATED)
