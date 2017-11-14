import functools

import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from telectapi.models import User


def auth(f):
    def wrapper(*args, **kwargs):
        try:
            user = User.from_token(args[1].META['HTTP_AUTHORIZATION'])
        except (jwt.exceptions.DecodeError, ValueError, ObjectDoesNotExist):
            return Response(status=401, data={"message": "unauthorized"})
        args[1].user = user
        return f(*args, **kwargs)

    return wrapper
