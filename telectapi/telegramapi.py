import os
from random import randint

from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.types import PeerChannel

from telectapi.models import User


# todo:: write a method that khodesh tasmim begire ke new kone ya session e salem darim!


class TelegramApi:
    SESSIONS_DIR = 'sessions'
    SESSIONS_PREFIX = 'session_'
    generated_sessions_dir = ''

    def __init__(self):
        self.generated_sessions_dir = os.path.join(os.path.dirname(__file__), self.SESSIONS_DIR)
        if not os.path.exists(self.generated_sessions_dir):
            os.makedirs(self.generated_sessions_dir)

    @staticmethod
    def get_app_data():
        return 159815, '82fc6a683d3434eb4c217a4b8bb10442'  # 922

        # return {  #935
        #     113161,
        #     '914d0e65dfcdfc54caa23666efd4134c'
        # }

    def connect_test_server(self):
        api_id, api_hash = self.get_app_data()

        client = TelegramClient(None, api_id, api_hash)
        client.session.server_address = '149.154.167.40'
        client.connect()

        dc_id = '2'  # Change this to the DC id of the test server you chose
        phone = '99966' + dc_id + str(randint(1000, 9999)).zfill(4)
        client.send_code_request(phone)
        client.sign_up(dc_id * 5, 'Some', 'Name')

        return client

    def sigh_in_cli(self, user, session=None):
        """

        :param str session:
        :param User|str user:
        :return: TelegramClient
        """
        api_id, api_hash = self.get_app_data()
        print(api_id)
        print(api_hash)
        if user is None:
            print("empty user!")
            return None
        if type(user) == User:
            mobile = user.mobile
        else:
            mobile = user

        if session is None:
            session = self.make_session(user)
        else:
            session = self.generated_sessions_dir + '/' + session
        print(session)

        client = TelegramClient(session, api_id, api_hash)
        client.connect()

        client.sign_in(phone=mobile)
        code = input('Enter code:')
        client.sign_in(code=code)

        return client

    def make_session(self, user):
        """

        :param User|str user:
        :return: str
        """
        if type(user) == User:
            mobile = user.mobile
        else:
            mobile = user
        return self.generated_sessions_dir + '/' + self.SESSIONS_PREFIX + str(mobile[-10:])

    def get_new_session(self, user):
        """

        :param User|str user:
        :return: TelegramClient
        """
        api_id, api_hash = self.get_app_data()
        print(api_id)
        print(api_hash)
        if user is None:
            print("empty user!")
            return None

        session = self.make_session(user)
        print(session)

        client = TelegramClient(session, api_id, api_hash)
        client.connect()

        return client

    def get_existing_session(self, user=None, session=None):
        """

        :param None|str session:
        :param User user:
        :return: TelegramClient
        """
        api_id, api_hash = self.get_app_data()

        if session is None:
            session = self.make_session(user)
        else:
            session = self.generated_sessions_dir + '/' + session
        client = TelegramClient(session, api_id, api_hash)
        client.connect()
        return client

    def get_channel(self, client, channel_id):
        """

        :param TelegramClient client:
        :param int channel_id:
        :return:
        """
        return client.get_entity(PeerChannel(channel_id))

    def create_channel(self, client, title, about):
        return client(CreateChannelRequest(title=title, about=about))

    def get_sys_sender_client(self):
        """
        :return: TelegramClient
        """
        return TelegramApi().get_existing_session(session="sys_client_922")
