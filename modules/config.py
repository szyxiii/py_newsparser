import json

from telethon.sync import TelegramClient


class Config:
    def __init__(self, filename):
        self.filename = filename
        # self.smtp = {}
        self.telegram = {}
        self.mongo = {}

        self._read_config()

    def _read_config(self):
        with open(self.filename) as file:
            self.content = json.load(file)

        # smtp = self.content['smtp']
        # self.smtp = smtp

        # print("\n[SMTP]\nLogin: {}\nPassword: {}\nHost: {}\nPort: {}".format(
        #     smtp['login'], '*' * len(smtp['password']), smtp['host'], smtp['port']))

        telegram = self.content['telegram']
        self.telegram = telegram

        print("[Telegram]\nApi id: {}\nApi hash: {}\nSession: {}\nRecipient: {}".format(telegram['api_id'], telegram['api_hash'], telegram['session'], telegram['recipient']))

        mongo = self.content['mongo']
        self.mongo = mongo

        print("\n[MongoDB]\nHost: {}\nPort: {}".format(mongo['host'], mongo['port']))
