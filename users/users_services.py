from datetime import timedelta
import jwt

from django.conf import settings

from rest_framework import status
from rest_framework.views import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode, User
from .utils import EmailUtil

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),    
    }

def validate_user(data):
    email = data['email']
    password = data['password']
    user = User.objects.filter(email = email).first()
    if user is None:
        return Response({'Error':'No user with this username'}, status.HTTP_404_NOT_FOUND)
    if not user.check_password(password):
        return Response({'Error':'Wrong password!'}, status=status.HTTP_400_BAD_REQUEST)
    return user

def get_user_by_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    user = User.objects.get(id=payload['user_id'])
    return user

def _create_or_change_confirmation_code(method, user, token):
    if method == 'signup':
        ConfirmationCode.objects.create(user = user, code = str(token))
    elif method == 'resend':
        user_code = ConfirmationCode.objects.get(user = user)
        user_code.code = str(token)
        user_code.save()

def create_token_and_send_to_email(user, method):
    token = RefreshToken().for_user(user).access_token
    token.set_exp(lifetime=timedelta(minutes=5))
    _create_or_change_confirmation_code(method, user, token)
    
    data = {'token':str(token),
            'to_email': user.email,
            'email_subject':'Verify your email'}
    EmailUtil.send_email(data)