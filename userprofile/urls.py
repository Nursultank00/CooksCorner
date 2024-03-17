from django.urls import path

from .views import UserProfileAPIView

urlpatterns = [
    path('<slug:slug>/', UserProfileAPIView.as_view(), name = 'profile-detail'),
]