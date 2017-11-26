import logging

from django.core.management import BaseCommand  # The class must be named Command, and subclass BaseCommand
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = "425588940:AAH561eu_J0YOi78BDNnAp48No2th_FFY0A"


class Command(BaseCommand):
    help = "Bot listen!"

    def handle(self, *args, **options):
        updater = Updater(token)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.start))
        dp.add_handler(CommandHandler("auth", self.auth,
                                      pass_args=True))

        dp.add_error_handler(self.error)
        updater.start_polling()
        updater.idle()

    @staticmethod
    def start(bot, update):
        update.message.reply_text('Hi! Send your mobile: /auth +989*********')

    @staticmethod
    def auth(bot, update, args):
        print("update:", update)
        print("args:", args)
        update.message.reply_text('Now send received code: /code +989********* *****')

    @staticmethod
    def code(bot, update, args):
        print("update:", update)
        print("args:", args)
        update.message.reply_text('Now send received code: /code +989********* *****')

    @staticmethod
    def password(bot, update, args):
        print("update:", update)
        print("args:", args)
        update.message.reply_text('Now send received code: /code +989********* *****')


    @staticmethod
    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)
