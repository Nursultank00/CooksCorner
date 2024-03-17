from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProfileSerializer
from .models import UserProfile, User

# Create your views here.

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "подробную информацию "
                              "о пользователе.",                    
        responses = {
            200: ProfileSerializer,
            404: "User profile is not found.",
        },
    )
    def get(self, request, slug, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность обновить "
                              "подробную информацию "
                              "о пользователе.",
        request_body = ProfileSerializer,                      
        responses = {
            200: ProfileSerializer,
            400: "Invalid data.",
            404: "User profile is not found.",
        },
    )
    def put(self, request, slug, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.update(profile, serializer.validated_data)
            return Response({'Message':'User profile is successfully updated.'}, status=status.HTTP_200_OK)
        return Response({'Error':'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)


class UserFollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность начать "
                              "отслежить другого "
                              "пользователя.",         
        responses = {
            200: "Success.",
            400: "Invalid data.",
            404: "User profile is not found.",
        },
    )
    def put(self, request, slug, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        user.profile.following.add(profile.user)
        return Response({'Message':'Success.'}, status=status.HTTP_200_OK)
    
class UserUnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность перестать "
                              "отслежить другого "
                              "пользователя.",         
        responses = {
            200: "Success.",
            400: "Invalid data.",
            404: "User profile is not found.",
        },
    )
    def put(self, request, slug, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        user.profile.following.remove(profile.user)
        return Response({'Message':'Success.'}, status=status.HTTP_200_OK)
