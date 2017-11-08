from time import sleep

from django.http import HttpResponse
from telethon.tl.functions.messages import GetAllChatsRequest, SearchGlobalRequest, ForwardMessagesRequest
from telethon.tl.types import Channel, InputPeerEmpty

from telegram.models import Source, User
from telegram.telegram import Telegram


def index(request):
    return HttpResponse("Hello world!")


def col(request):
    user = User.objects.get(id=1111111111)
    # client = Telegram().sigh_in_org(user)
    client = Telegram().get_existing_session(user)

    result = client(GetAllChatsRequest([]))
    for chat in result.chats:
        print(type(chat))
        if type(chat) == Channel:
            print(chat)
            if chat.username is not None:
                client(SearchGlobalRequest(q=chat.username, limit=10, offset_date=None, offset_id=0,
                                           offset_peer=InputPeerEmpty()))

                src = Source.objects.create(collection_id=1, type=Source.TELEGRAM,
                                            source_data={'id': chat.id,
                                                         'username': chat.username})
                print('New id:', src.id)

    return HttpResponse(result.count())


def send(request):
    tg = Telegram()
    for user in User.objects.all():
        client = tg.get_existing_session(user)
        for collection in user.collection_set.all():
            dest_chan = tg.get_channel(client, collection.destination_data['id'])
            for source in collection.source_set.all():
                print(source)
                channel = tg.get_channel(client, source.source_data['id'])  # result is in descending sort
                sleep(1)
                total, messages, senders = client.get_message_history(channel, limit=50)
                messages = messages[::-1]
                for msg in messages:
                    # print("msg.date.timestamp():", msg.date.timestamp())
                    # print("source.last_fm_time.timestamp():", source.last_fm_time.timestamp())
                    if msg.date.timestamp() > source.last_fm_time.timestamp():
                        print("are")
                        client(ForwardMessagesRequest(
                            from_peer=channel,
                            id=[msg.id],
                            to_peer=dest_chan
                        ))
                        source.last_fm_time = msg.date
                        source.last_fm_id = msg.id
                        source.save()

    # return HttpResponse(200)
