import re

from django.core.exceptions import ValidationError
from django.utils import timezone

REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')
YEAR_GREATER_THAN_CURRENT = 'Год %(value)s больше текущего!'
ME_USER = 'Имя пользователя "me" использовать нельзя!'
ALLOWED_CHARACTERS = 'Можно использовать только буквы, цифры и "@.+-_".'


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            YEAR_GREATER_THAN_CURRENT,
            params={'value': value},
        )


def validate_username(name):
    if name == 'me':
        raise ValidationError(ME_USER)
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(ALLOWED_CHARACTERS)
