from telethon.sync import TelegramClient


class Telegram:
    def __init__(self, session, api_id, api_hash):
        self.session = session
        self.api_id = api_id
        self.api_hash = api_hash

        self.client = None

    def connect(self):
        self.client = TelegramClient(self.session, self.api_id, self.api_hash)
        self.client.start()
