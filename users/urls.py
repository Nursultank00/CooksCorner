from django.urls import path, include

# from users.views import SignupAPIView, LoginAPIView, TokenRefreshView,\
#                         LogoutAPIView, VerifyEmailAPIView, ResendVerifyEmailAPIView,\
#                         DeleteUserAPIView, ChangePasswordAPIView

# urlpatterns = [
#     path('login/', LoginAPIView.as_view(), name = 'cookscorner-login'),
#     path('login/refresh/', TokenRefreshView.as_view(), name = 'cookscorner-login-refresh'),
#     path('signup/', SignupAPIView.as_view(), name = 'cookscorner-signup'),
#     path('logout/', LogoutAPIView.as_view(), name = 'cookscorner-logout'),
#     path('email-verify/', VerifyEmailAPIView.as_view(), name = 'cookscorner-email-verify'),
#     path('resend-email/', ResendVerifyEmailAPIView.as_view(), name = 'cookscorner-resend-email'),
#     path('delete-user/', DeleteUserAPIView.as_view(), name = 'cookscorner-delete'),
#     path('change-password/', ChangePasswordAPIView.as_view(), name = 'cookscorner-change-password'),
#     path('password-reset/', include('django_rest_passwordreset.urls'), name='cookscorner-password_reset'),
# ]