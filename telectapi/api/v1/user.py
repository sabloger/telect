from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from telethon.tl.types.auth import SentCode

from telectapi import models
from telectapi.models import AuthTemp
from telectapi.telegramapi import TelegramApi


class User(viewsets.ViewSet):
    parser_classes = (JSONParser,)

    @list_route(methods=['post'])
    def auth(self, request):
        """

        :param Request request:
        :return:
        """
        # todo: check user existing and session existing
        # bug: PhoneNumberUnoccupiedError new register
        mobile = request.data.get('mobile', None)
        code = request.data.get('code', None)

        if mobile is None:
            return Response(data={"message": "invalid_or_empty_mobile"}, status=400)

        tg = TelegramApi()
        client = tg.get_new_session(mobile)

        if not client.is_user_authorized():
            if code is None:
                scres = client.sign_in(phone=mobile)
                if type(scres) == SentCode:
                    AuthTemp.objects.create(mobile=mobile, phone_code_hash=scres.phone_code_hash)
                    return Response(status=200, data={"message": "waiting_for_code"})
                else:
                    return Response(status=400, data={"message": "error"})
            else:
                at = AuthTemp.objects.get(mobile=mobile, is_used=False)  # todo: check date
                if at is None:
                    return Response(status=400, data={"message": "mobile_not_found"})
                else:
                    at.is_used = True
                    at.save()

                resl = client.sign_in(phone=mobile, code=code, phone_code_hash=at.phone_code_hash)
                print("resl:", resl)
        try:
            user = models.User.objects.get(mobile=mobile)
            user.session_name = tg.make_session(mobile)
            user.save()
        except ObjectDoesNotExist:
            user = models.User.objects.create(mobile=mobile, session_name=tg.make_session(mobile))

        jr = JsonResponse(client.get_me().to_dict())
        jr['Authorization'] = user.make_token()
        client.disconnect()
        return jr
