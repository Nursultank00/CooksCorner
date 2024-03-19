from datetime import timedelta
import jwt

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode, ChangePasswordCode, User
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

def get_user_by_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    user = User.objects.get(id=payload['user_id'])
    return user

def _create_or_change_code(user, token, model):
    user_check = model.objects.filter(user = user).first()
    if user_check is None:
        model.objects.create(user = user, code = str(token))
    else:
        user_code = model.objects.get(user = user)
        user_code.code = str(token)
        user_code.save()

def create_token_and_send_to_email(user, query, url):
    token = RefreshToken().for_user(user).access_token
    token.set_exp(lifetime=timedelta(minutes=5))
    if query == 'verify-account':
        model = ConfirmationCode
        html = 'users/email.html'
        email_subject = 'Verify your email'
    elif query == 'change-password':
        model = ChangePasswordCode
        html = 'users/forgot_password.html'
        email_subject = 'Change password'
    _create_or_change_code(user, token, model)
    data = {'token':str(token),
            'to_email': user.email,
            'email_subject': email_subject}
    EmailUtil.send_email(data, url, html)