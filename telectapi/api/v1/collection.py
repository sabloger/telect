from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from telectapi.api.base import auth


class Collection(viewsets.ViewSet):
    @auth
    def list(self, request):
        """

        :param Request request:
        :return:
        """

        return Response(request.user.mobile)
