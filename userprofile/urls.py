from django.urls import path

from .views import (
                    UserProfileAPIView,
                    UserFollowAPIView,
                    SearchUsersAPIView,
)

urlpatterns = [
    path('detail/<slug:slug>/', UserProfileAPIView.as_view(), name = 'profile-detail'),
    path('follow/<slug:slug>/', UserFollowAPIView.as_view(), name = 'follow-user'),
    path('search/', SearchUsersAPIView.as_view(), name = 'search-users'),
]