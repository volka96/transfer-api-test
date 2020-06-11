from datetime import timedelta
from typing import Union

from django.contrib.auth import get_user_model
from django.utils import timezone
from knox.models import AuthToken
from knox.settings import knox_settings

User = get_user_model()


def _get_token_limit_per_user(token_limit: Union[int, None]) -> Union[int, None]:
    return token_limit if token_limit is not None else knox_settings.TOKEN_LIMIT_PER_USER


def generate_token(user: User, ttl: timedelta = None, token_limit: int = None):
    token_limit_per_user = _get_token_limit_per_user(token_limit)
    if token_limit_per_user is not None:
        now = timezone.now()
        token = user.auth_token_set.filter(expiry__gt=now)
        if token.count() >= token_limit_per_user:
            raise RuntimeError("Maximum amount of tokens allowed per user exceeded.")
    instance, token = AuthToken.objects.create(user, ttl)

    return {
        'expiry': instance.expiry,
        'token': token
    }
