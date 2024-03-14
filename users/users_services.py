from datetime import timedelta

from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode
from .utils import EmailUtil

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