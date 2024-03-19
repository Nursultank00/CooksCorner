from datetime import timedelta
import jwt

from django.conf import settings

from rest_framework import status
from rest_framework.views import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode, User
from .utils import EmailUtil

def destroy_token(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),    
    }

def validate_user(data):
    email = data['email']
    password = data['password']
    user = User.objects.filter(email = email).first()
    if user is None:
        return Response({'Error':'No user with this email.'}, status.HTTP_404_NOT_FOUND)
    if not user.check_password(password):
        return Response({'Error':'Wrong password!'}, status=status.HTTP_400_BAD_REQUEST)
    return user

def get_user_by_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    user = User.objects.get(id=payload['user_id'])
    return user

def _create_or_change_confirmation_code(user, token):
    user_check = ConfirmationCode.objects.filter(user = user).first()
    if user_check is None:
        ConfirmationCode.objects.create(user = user, code = str(token))
    else:
        user_code = ConfirmationCode.objects.get(user = user)
        user_code.code = str(token)
        user_code.save()

def create_token_and_send_to_email(user):
    token = RefreshToken().for_user(user).access_token
    token.set_exp(lifetime=timedelta(minutes=5))
    _create_or_change_confirmation_code(user, token)
    
    data = {'token':str(token),
            'to_email': user.email,
            'email_subject':'Verify your email'}
    EmailUtil.send_email(data)