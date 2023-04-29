import re

from django.core.exceptions import ValidationError
from django.utils import timezone

REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )


def validate_username(name):
    if name == 'me':
        raise ValidationError('Имя пользователя "me" использовать нельзя!')
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(
            'Можно использовать только буквы, цифры и "@.+-_".')
