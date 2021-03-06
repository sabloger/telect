import os
from datetime import timedelta
from random import randint

from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, ChatAdminRequiredError
from telethon.tl.functions.channels import CreateChannelRequest, EditAdminRequest, ExportInviteRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import PeerChannel, ChannelAdminRights, InputUser

from telectapi.models import User


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
        return 129003, 'cf7558e59798a134a0181496e35d8c39'  # mahsa 937
        # return 159815, '82fc6a683d3434eb4c217a4b8bb10442'  # 922 XX fucked
        # return 113161, '914d0e65dfcdfc54caa23666efd4134c'  # 935 XX fucked

    def connect_test_server(self):
        api_id, api_hash = self.get_app_data()

        client = TelegramClient(None, api_id, api_hash, timeout=timedelta(seconds=10))
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

        client = TelegramClient(session, api_id, api_hash, timeout=timedelta(seconds=10))
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
        client = TelegramClient(session, api_id, api_hash, timeout=timedelta(seconds=10))
        client.connect()
        return client

    def get_session(self, user):
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

        client = TelegramClient(session, api_id, api_hash, timeout=timedelta(seconds=10))
        client.connect()

        return client

    def get_channel(self, client, channel_id):
        """

        :param TelegramClient client:
        :param int channel_id:
        :return:
        """
        return client.get_entity(PeerChannel(channel_id))

    def make_about(self, sources):
        """

        :param  sources:
        :return:
        """
        about = "Channels:"
        for source in sources:
            about += "\n@" + source.source_data['username']

        # about += "\nLast update:\n" + timezone.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
        about += "\n" + str(randint(0, 999))
        return about

    def get_dest_channel_old(self, owner_client, client, channel_id, sources):
        """

        :param sources:
        :param TelegramClient owner_client:
        :param TelegramClient client:
        :param int channel_id:
        :return: Channel
        """
        try:
            channel = client.get_entity(PeerChannel(channel_id))
            print("get_dest_channel 1 channel:", channel)
            exit(1)
            client(ExportInviteRequest(channel))
            # try:
            #     client(EditAboutRequest(channel, self.get_about(sources)))
            # except Exception as e:
            #     print("error:", e)
            #     pass
            # todo:: check the owner is in the channel members
            # todo:: check members count
            # todo:: set list of sources to the about
            return channel
        except (ValueError, ChannelPrivateError) as e:
            owner_channel = owner_client.get_entity(PeerChannel(channel_id))
            inv = owner_client(ExportInviteRequest(owner_channel))
            client(ImportChatInviteRequest(inv.link.split('/')[-1]))
            channel = client.get_entity(PeerChannel(channel_id))
            print("e:", e)
            print("get_dest_channel 2 channel:", channel)
            exit(1)
            sender = client.get_me()
            self.set_admin(owner_client, sender, owner_channel)
            return channel
        except ChatAdminRequiredError:
            owner_channel = owner_client.get_entity(PeerChannel(channel_id))
            sender = client.get_me()
            self.set_admin(owner_client, sender, owner_channel)
            channel = client.get_entity(PeerChannel(channel_id))

            print("get_dest_channel 3 channel:", channel)
            exit(1)
            return channel

    def get_dest_channel(self, owner_client, client, channel_id, sources):
        """

        :param sources:
        :param TelegramClient owner_client:
        :param TelegramClient client:
        :param int channel_id:
        :return: Channel
        """
        try:
            channel = client.get_entity(PeerChannel(channel_id))

            if channel.admin_rights is None or not channel.admin_rights.post_messages or not channel.admin_rights.invite_link:
                owner_channel = owner_client.get_entity(PeerChannel(channel_id))
                sender = client.get_me()
                self.set_admin(owner_client, sender, owner_channel)

            return channel
        except (ValueError, ChannelPrivateError):
            owner_channel = owner_client.get_entity(PeerChannel(channel_id))
            inv = owner_client(ExportInviteRequest(owner_channel))
            client(ImportChatInviteRequest(inv.link.split('/')[-1]))
            channel = client.get_entity(PeerChannel(channel_id))

            sender = client.get_me()
            self.set_admin(owner_client, sender, owner_channel)
            return channel

    def set_admin(self, owner_client, sender, owner_channel):
        owner_client(
            EditAdminRequest(channel=owner_channel, user_id=InputUser(sender.id, sender.access_hash),
                             admin_rights=ChannelAdminRights(
                                 change_info=True,
                                 post_messages=True,
                                 edit_messages=True,
                                 delete_messages=True,
                                 ban_users=True,
                                 invite_users=True,
                                 invite_link=True,
                                 pin_messages=True,
                                 add_admins=True,
                             )))

    def create_channel(self, client, title, about):
        return client(CreateChannelRequest(title=title, about=about))

    def get_sys_sender_client(self):
        """
        :return: TelegramClient
        """
        # return TelegramApi().get_existing_session(session="sys_client_922")
        return self.get_session("+989227253035")
