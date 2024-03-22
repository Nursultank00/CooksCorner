import re

from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _
from django.template.loader import render_to_string

# Overriding email field of the model
class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value


# Email send function
class EmailUtil:
    """
    Email sending class
    """
    @staticmethod
    def send_email(data, url, html):
        context ={
            'link_app': ''.join(url)+data['token']
        }
        html_content = render_to_string(
            html, context=context
        )
        email = EmailMultiAlternatives(subject = data['email_subject'], to = [data['to_email']])
        email.attach_alternative(html_content, "text/html")
        email.send()

# Password Validators
class LengthValidator:
    def __init__(self, min_length=8, max_length=15):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must contain at least %(min_length)d characters."),
                code="password_too_short",
                params={"min_length": self.min_length},
            )
        if len(password) > self.max_length:
            raise ValidationError(
                _("The password's length must be lower than %(max_length)d characters."),
                code="password_too_long",
                params={"max_length": self.max_length+1},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters and lower than %(max_length)d characters."
            % {"min_length": self.min_length,
               "max_length": self.max_length+1}
        )

class DigitValidator:
    def __init__(self):
        pass

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("The password must contain at least 1 numeric character."),
                code="no numeric character"
            )

    def get_help_text(self):
        return _(
            "Your password must contain numeric character."
        )
    
class UpperLowerValidator:
    def __init__(self):
        pass

    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("The password must contain at least 1 upper case character."),
                code="no upper case character"
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("The password must contain at least 1 lower case characters."),
                code="no lower case character"
            )

    def get_help_text(self):
        return _(
            "Your password must contain upper case and lower case characters."
        )
    
class SpecialCharacterValidator:
    def __init__(self):
        pass

    def validate(self, password, user=None):
        if not re.search(r'[-_!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("The password must contain at least 1 special case character."),
                code="no special character"
            )

    def get_help_text(self):
        return _(
            "Your password must contain special characters."
        )
    