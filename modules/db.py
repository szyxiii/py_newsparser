from pymongo import MongoClient


class DB:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port

        self.client = None
        self.db = None
        self.news = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client['project']
        self.news = self.db['news']

    def close(self):
        self.client.close()
