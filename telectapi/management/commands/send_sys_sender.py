from datetime import datetime
from time import sleep

from django.core.management import BaseCommand  # The class must be named Command, and subclass BaseCommand
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import ForwardMessagesRequest

from telectapi.models import User
from telectapi.telegramapi import TelegramApi


class Command(BaseCommand):
    # Show this when the user types help
    help = "Send messages!"

    # A command must define handle()
    def handle(self, *args, **options):
        print("Started:", datetime.now())
        tg = TelegramApi()
        sys_sender_client = tg.get_sys_sender_client()
        for user in User.objects.all():
            client = tg.get_existing_session(user)
            for collection in user.collection_set.all():
                dest_chan = tg.get_channel(sys_sender_client, collection.destination_data['id'])
                for source in collection.source_set.all():
                    print(source)
                    try:
                        channel = tg.get_channel(sys_sender_client,
                                                 source.source_data['id'])  # result is in descending sort
                    except ValueError:
                        sys_sender_client(ResolveUsernameRequest(source.source_data['username']))
                        channel = tg.get_channel(sys_sender_client,
                                                 source.source_data['id'])  # result is in descending sort

                    sleep(1)
                    total, messages, senders = client.get_message_history(channel, limit=20)
                    messages = messages[::-1]
                    for msg in messages:
                        if msg.date.timestamp() > source.last_fm_time.timestamp():
                            print("are")
                            sys_sender_client(ForwardMessagesRequest(
                                from_peer=channel,
                                id=[msg.id],
                                to_peer=dest_chan
                            ))
                            source.last_fm_time = msg.date
                            source.last_fm_id = msg.id
                            source.save()
        self.stdout.write("Doing All The Things!")
