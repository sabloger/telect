from telegram.ext import Updater
from telethon.tl import types


class TelegramSenderBot:
    token = "425588940:AAH561eu_J0YOi78BDNnAp48No2th_FFY0A"
    updater = Updater(token)
    dest_chan_id = None
    msg = None

    def __init__(self, dest_chan_id, msg):
        if str(dest_chan_id).index('-100') != 0:
            raise ValueError("error in dest_chan_id %s" % dest_chan_id)
        if type(msg) != types.Message:
            raise ValueError("error in msg %s" % msg)

        self.dest_chan_id = dest_chan_id
        self.msg = msg

    @staticmethod
    def send(dest_chan_id, msg):
        self = TelegramSenderBot(dest_chan_id, msg)
        invokers = {
            types.MessageMediaPhoto: self.photo,
            types.MessageMediaEmpty: self.text,
            types.MessageMediaDocument: self.document,
            types.MessageMediaWebPage: self.webpage,
            type(None): self.text,
        }

        print("Type:", type(msg.media))
        invokers[type(msg.media)]()

        # res = self.updater.bot.sendMessage(
        #     chat_id=int("-100" + str(collection.destination_data['id'])),
        #     text=msg.media.caption)
        # self.stdout.write(res.caption)

    def photo(self):

        # print(self.msg.media.to_dict()['photo'])
        res = self.updater.bot.send_photo(
            chat_id=self.dest_chan_id,
            text=self.msg.media.caption,
            photo=self.msg.media.to_dict()['photo']
        )
        print("response:", res.stringify())

    def text(self):
        res = self.updater.bot.send_photo(
            chat_id=self.dest_chan_id,
            text=self.msg.text
        )
        print("response:", res.stringify())

    def document(self):
        res = self.updater.bot.send_document(
            chat_id=self.dest_chan_id,
            text=self.msg.media.caption,
            document=self.msg.media.document.id
        )
        print("response:", res.stringify())

    def webpage(self):
        pass
