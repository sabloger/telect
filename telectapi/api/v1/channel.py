from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from telethon.tl.functions.messages import GetAllChatsRequest
from telethon.tl.types import Channel

from telectapi.api.base import auth
from telectapi.telegramapi import TelegramApi


class TgChannel(viewsets.ViewSet):
    @auth
    def list(self, request):
        """

        :param Request request:
        :return:
        """

        client = TelegramApi().get_existing_session(request.user)

        result = client(GetAllChatsRequest([]))
        res_final = []
        for chat in result.chats:
            if type(chat) == Channel:
                if chat.username is not None:
                    res_final.append(chat.to_dict())
                    print(chat.username)
        return Response(res_final)
