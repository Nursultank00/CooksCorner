from django.urls import path

from .views import (
                    UserProfileAPIView,
                    UserFollowAPIView,
                    UserUnfollowAPIView
)

urlpatterns = [
    path('<slug:slug>/', UserProfileAPIView.as_view(), name = 'profile-detail'),
    path('<slug:slug>/follow/', UserFollowAPIView.as_view(), name = 'follow-user'),
    path('<slug:slug>/unfollow/', UserUnfollowAPIView.as_view(), name = 'unfollow-user'),
]