# -*- encoding=UTF-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response

from telectapi import models
from telectapi.api.base import auth
from telectapi.telegramapi import TelegramApi


class Collection(viewsets.ViewSet):
    parser_classes = (JSONParser,)

    @auth
    def list(self, request):
        """

        :param Request request:
        :return:
        """

        collections = models.Collection.objects.filter(user=request.user)
        return Response(collections.values())

    @auth
    def create(self, request):
        """

        :param Request request:
        :return:
        """
        if "channels" not in request.data or len(request.data["channels"]) == 0:
            return Response(status=400, data={"message": "empty_channel_list"})

        name = "TTL " + request.data.get("name", "")

        tg = TelegramApi()
        client = tg.get_existing_session(request.user)
        collection_dest = tg.create_channel(client, name, "this is a test chan from python!!!")

        print(collection_dest.to_dict())
        collection = models.Collection.objects.create(name=name, destination_type=models.Collection.TELEGRAM,
                                                      destination_data={"id": collection_dest.chats[0].id},
                                                      user=request.user)

        for channel in request.data["channels"]:
            if type(channel) != dict or "id" not in channel or "username" not in channel:
                return Response(status=400, data={"message": "invalid channel", "channel": channel})
            models.Source.objects.create(source_data=channel, collection=collection)
        return Response({'collection': collection.id})

    @detail_route(methods=['post'])
    @auth
    def add_source(self, request, pk):
        if "channels" not in request.data or len(request.data["channels"]) == 0:
            return Response(status=400, data={"message": "empty_channel_list"})

        collection = models.Collection.objects.get(id=pk)

        for channel in request.data["channels"]:
            if type(channel) != dict or "id" not in channel or "username" not in channel:
                return Response(status=400, data={"message": "invalid channel", "channel": channel})

            sources = models.Source.objects.filter(source_data__contains={'id': channel['id']}, collection=collection)
            if len(sources) == 0:
                models.Source.objects.create(source_data=channel, collection=collection)

        return Response({'collection': collection.id})

    @detail_route(methods=['delete'])
    @auth
    def del_source(self, request, pk):
        if "channels" not in request.data or len(request.data["channels"]) == 0:
            return Response(status=400, data={"message": "empty_channel_list"})

        collection = models.Collection.objects.get(id=pk)

        for channel in request.data["channels"]:
            if type(channel) != dict or "id" not in channel or "username" not in channel:
                return Response(status=400, data={"message": "invalid channel", "channel": channel})

            sources = models.Source.objects.filter(source_data__contains={'id': channel['id']}, collection=collection)
            sources.delete()

        return Response({'collection': collection.id})
