from time import sleep

from django.core.management import BaseCommand  # The class must be named Command, and subclass BaseCommand
from django.utils import timezone
from telegram.ext import Updater

from telectapi.models import User
from telectapi.telegram_sender_bot import TelegramSenderBot
from telectapi.telegramapi import TelegramApi


class Command(BaseCommand):
    # Show this when the user types help
    help = "Send messages!"
    token = "425588940:AAH561eu_J0YOi78BDNnAp48No2th_FFY0A"
    updater = Updater(token)

    # A command must define handle()
    def handle(self, *args, **options):
        print("Started:", timezone.now())
        tg = TelegramApi()
        for user in User.objects.all():
            client = tg.get_existing_session(user)
            for collection in user.collection_set.all():
                # dest_chan = tg.get_channel(client, collection.destination_data['id'])
                for source in collection.source_set.all():
                    print(source)
                    channel = tg.get_channel(client, source.source_data['id'])  # result is in descending sort
                    sleep(1)
                    total, messages, senders = client.get_message_history(channel, limit=1)
                    messages = messages[::-1]
                    for msg in messages:
                        # print("msg.date.timestamp():", msg.date.timestamp())
                        # print("source.last_fm_time.timestamp():", source.last_fm_time.timestamp())
                        if msg.date.timestamp() > source.last_fm_time.timestamp() or True:
                            print("are")
                            # client(ForwardMessagesRequest(
                            #     from_peer=channel,
                            #     id=[msg.id],
                            #     to_peer=dest_chan
                            # ))

                            TelegramSenderBot.send(int("-100" + str(collection.destination_data['id'])), msg)

                            source.last_fm_time = msg.date
                            source.last_fm_id = msg.id
                            source.save()
        self.stdout.write("Doing All The Things!")
