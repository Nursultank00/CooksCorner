from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProfileSerializer
from .models import UserProfile
from .services import get_paginated_data
from .swagger import (
                        search_user_swagger,
                        user_detail_swagger,
                        myprofile_swagger,
)
# Create your views here.

class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "подробную информацию "
                              "о себе.",          
        responses = {
            200: myprofile_swagger['response']
        },
    )
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, context = {'detail':True,
                                                           'user': request.user,
                                                            'me': True})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность обновить "
                              "свою подробную информацию.",
        request_body = myprofile_swagger['request_body'],                      
        responses = {
            200: "Profile has been successfully changed.",
            400: "Invalid data."
        },
    )
    def put(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data = request.data, context = {'detail': False,
                                                                                'user': request.user,
                                                                                'me': True})
        if serializer.is_valid():
            serializer.update(profile, serializer.validated_data)
            return Response({'Message':'Profile has been successfully changed.'}, status=status.HTTP_200_OK)
        return Response({'Error':'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность получить "
                              "подробную информацию "
                              "о пользователе по slug. ",                    
        responses = {
            200: user_detail_swagger['response'],
            404: "User profile is not found.",
        },
    )
    def get(self, request, slug, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(slug = slug)
        except Exception:
            return Response({'Error':'User profile is not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, context = {'detail': True,
                                                           'user': request.user,
                                                           'me': False})
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
            400: "You can't follow yourself",
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
        if user.profile == profile:
            return Response({"Error": "You can't follow yourself"}, status = status.HTTP_400_BAD_REQUEST)
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
        tags=['User profile'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность найти рецепт по названию. ",
        manual_parameters = search_user_swagger['parameters'],
        responses = {
            200: search_user_swagger['response'],
        },
    )
    def get(self, request, *args, **kwargs):
        queryset = UserProfile.objects.all()
        queryset = self.filter_queryset(queryset)
        data = get_paginated_data(queryset, request)
        return Response(data, status = status.HTTP_200_OK)