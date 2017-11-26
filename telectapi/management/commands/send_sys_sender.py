import threading
from datetime import datetime
from time import sleep

from django.core.management import BaseCommand  # The class must be named Command, and subclass BaseCommand
from telethon.errors import ChannelInvalidError
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.types import Message

from telectapi.models import User, Source
from telectapi.telegramapi import TelegramApi


class Command(BaseCommand):
    # Show this when the user types help
    help = "Send messages!"

    # A command must define handle()
    def handle(self, *args, **options):
        print("Started:", datetime.now())

        telegram_api = TelegramApi()
        sys_sender_client = telegram_api.get_sys_sender_client()

        for user in User.objects.all():
            print("user:", user)

            try:

                user_client = telegram_api.get_existing_session(user)
                print(user.collection_set.all())
            except:
                continue

            for collection in user.collection_set.all():
                # self.send_collection(collection, telegram_api, user_client, sys_sender_client)
                sleep(1)
                t = threading.Thread(target=self.send_collection,
                                     args=(collection, telegram_api, user_client, sys_sender_client))
                t.start()

        self.stdout.write("End of work!")

    def send_collection(self, collection, telegram_api, user_client, sys_sender_client):
        print("collection:", collection)

        try:
            sources = collection.source_set.all()

            sleep(1)
            destination_chan = telegram_api.get_dest_channel(user_client, sys_sender_client,
                                                             collection.destination_data['id'],
                                                             sources)
        except:
            return

        for source in sources:
            try:
                try:
                    src = Source.objects.get(id=source.id, last_fm_time__gt=datetime.now().timestamp() - 30,
                                             are_collecting=True)
                    if src.are_collecting:
                        continue
                    else:
                        source.are_collecting = True
                        source.save()
                except:
                    source.are_collecting = True
                    source.save()

                print("collection:", collection, "source:", source)

                sleep(3)

                try:
                    channel = telegram_api.get_channel(sys_sender_client, source.source_data['id'])

                except ValueError:
                    sys_sender_client(ResolveUsernameRequest(source.source_data['username']))
                    channel = telegram_api.get_channel(sys_sender_client, source.source_data['id'])

                try:
                    total, messages, senders = user_client.get_message_history(channel, limit=20)

                except ChannelInvalidError:
                    try:
                        print("ChannelInvalidError:", source.source_data['username'])
                        user_client(ResolveUsernameRequest(source.source_data['username']))
                        total, messages, senders = user_client.get_message_history(channel, limit=20)

                    except:
                        source.are_collecting = False
                        source.save()
                        continue

                messages = messages[::-1]  # reversing list to be asc (because telegram desc mid)

                for msg in messages:
                    if type(msg) is Message:
                        if msg.date.timestamp() > source.last_fm_time.timestamp():
                            print("msg:", msg.id)

                            sleep(3)
                            sys_sender_client(ForwardMessagesRequest(
                                from_peer=channel,
                                id=[msg.id],
                                to_peer=destination_chan,
                                silent=True
                            ))

                            source.last_fm_time = msg.date
                            source.last_fm_id = msg.id
                            source.save()

                source.are_collecting = False
                source.save()
            except:
                source.are_collecting = False
                source.save()
