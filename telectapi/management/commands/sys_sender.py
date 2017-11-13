from datetime import datetime

from django.core.management import BaseCommand  # The class must be named Command, and subclass BaseCommand
from telethon.tl.functions.account import UpdateProfileRequest

from telectapi.telegramapi import TelegramApi


class Command(BaseCommand):
    # Show this when the user types help
    help = "Send messages!"

    # A command must define handle()
    def handle(self, *args, **options):
        print("Started:", datetime.now())
        # client = TelegramApi().sigh_in_org("+989227253035", "sys_client_922")
        client = TelegramApi().get_existing_session(session="sys_client_922")

        # client(UpdateUsernameRequest("telectbot"))
        # client(UpdateProfileRequest(first_name="ttlbot", last_name="BOT", about="ttl machine account"))
        self.stdout.write(client.get_me().stringify())
        self.stdout.write("Doing All The Things!")
