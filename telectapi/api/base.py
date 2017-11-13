import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from telectapi.models import User


def auth(func):
    def jwt_auth(obj, request):
        try:
            user = User.from_token(request.META['HTTP_AUTHORIZATION'])
        except (jwt.exceptions.DecodeError, ValueError, ObjectDoesNotExist):
            return Response(status=401, data={"message": "unauthorized"})
        request.user = user
        return func(obj, request)

    return jwt_auth
