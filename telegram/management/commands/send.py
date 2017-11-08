from datetime import datetime
from time import sleep

from django.core.management import BaseCommand  # The class must be named Command, and subclass BaseCommand
from telethon.tl.functions.messages import ForwardMessagesRequest

from telegram.models import User
from telegram.telegram import Telegram


class Command(BaseCommand):
    # Show this when the user types help
    help = "Send messages!"

    # A command must define handle()
    def handle(self, *args, **options):
        print("Started:", datetime.now())
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
        self.stdout.write("Doing All The Things!")
