import sys
import time

from modules.config import Config
from modules.db import DB
from modules.pyparser import YandexParser, GoogleParser
from modules.telegram import Telegram


def main(args):
    print("Считывается конфигурация...")
    cfg = Config("config.json")

    query = "Microsoft"

    if len(args) >= 1:
        cfg.mongo['host'] = args[0]

        if len(args) == 2:
            cfg.mongo['port'] = args[1]

        if len(args) == 3:
            query = args[2]

    # DataBase
    print("\nПодключение к mongodb://{}:{}".format(cfg.mongo['host'], cfg.mongo['port']))

    db = DB(cfg.mongo['host'], cfg.mongo['port'])
    db.connect()

    print("Подключение выполнено")

    # Telegram
    telegram = Telegram(cfg.telegram['session'], cfg.telegram['api_id'], cfg.telegram['api_hash'])
    telegram.connect()

    # Parsing
    gn = GoogleParser()
    news = gn.parse(query)

    print(f"Получено новостей: {len(news)}")

    db.news.delete_many({})
    db.news.insert_many(news)

    print("Новости выгружены в базу данных")

    news_per_message = 5
    message_delay = 1.5
    to_send = []

    start = 0
    for idx, item in enumerate(news):
        if idx % news_per_message != 0 or idx == 0:
            to_send.append('[{}] {} - {}'.format(idx + 1, item['title'], item['link']))
        elif idx % news_per_message == 0:
            time.sleep(message_delay)
            telegram.client.send_message(cfg.telegram['recipient'], "\n".join(to_send))
            to_send = ['[{}] {} - {}'.format(idx + 1, item['title'], item['link'])]

    if len(to_send):
        time.sleep(message_delay)
        telegram.client.send_message(cfg.telegram['recipient'], "\n".join(to_send))
        to_send = []


if __name__ == '__main__':
    main(sys.argv[1:])
