from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.request import Request


class User(viewsets.ViewSet):
    @staticmethod
    @list_route(methods=['post'])  # , permission_classes=[IsAdminOrIsSelf]
    def auth(request):
        """

        :param Request request:
        :return:
        """
