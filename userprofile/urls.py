from django.urls import path

from .views import (
                    UserProfileAPIView,
                    UserFollowAPIView,
                    SearchUsersAPIView,
                    MyProfileAPIView
)

urlpatterns = [
    path('detail/<slug:slug>/', UserProfileAPIView.as_view(), name = 'cookscorner-profile-detail'),
    path('follow/<slug:slug>/', UserFollowAPIView.as_view(), name = 'cookscorner-follow-user'),
    path('search/', SearchUsersAPIView.as_view(), name = 'cookscorner-search-users'),
    path('myprofile/', MyProfileAPIView.as_view(), name = 'cookscorner-myprofile')
]