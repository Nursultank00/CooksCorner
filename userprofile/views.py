from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProfileSerializer
from .models import UserProfile
from .services import get_paginated_data
# Create your views here.

class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "подробную информацию "
                              "о пользователе.",                    
        responses = {
            200: ProfileSerializer
        },
    )
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, context = {'detail':True})
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
            400: "Invalid data."
        },
    )
    @parser_classes((MultiPartParser,))
    def put(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data = request.data, context = {'detail': False})
        if serializer.is_valid():
            serializer.update(profile, serializer.validated_data)
            return Response({'Message':'User profile is successfully updated.'}, status=status.HTTP_200_OK)
        return Response({'Error':'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = ProfileSerializer(profile, context = {'detail': True})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            403: "User is not verified.",
            404: "User profile is not found.",
        },
    )
    def put(self, request, slug, *args, **kwargs):
        user = request.user
        if not user.is_verified:
            return Response({"Error": "User is not verified."}, status = status.HTTP_403_FORBIDDEN)
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        if profile in user.profile.following.all():
            user.profile.following.remove(profile)
        else:
            user.profile.following.add(profile)
        return Response({'Message':'Success.'}, status=status.HTTP_200_OK)
    
class SearchUsersAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность найти рецепт по названию. ",                
        responses = {
            200: ProfileSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        queryset = UserProfile.objects.all()
        queryset = self.filter_queryset(queryset)
        data = get_paginated_data(queryset, request)
        return Response(data, status = status.HTTP_200_OK)