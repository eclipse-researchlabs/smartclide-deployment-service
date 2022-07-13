import urllib.parse
from pymongo import MongoClient
from deployment_service.config.settings import Settings

class MongoRepo:
    def __init__(self, db_name='deployment_component', page_size=50 )-> None:
        settings = Settings()
        self.host = settings.repositories['mongo']['host']
        self.port = int(settings.repositories['mongo']['port'])
        self.user = urllib.parse.quote_plus(settings.repositories['mongo']['user'])
        self.password = urllib.parse.quote_plus(settings.repositories['mongo']['password'])
        db = self.__get_mongo_client(db_name)
        self.deployments_db = db.deployments

    def __get_mongo_client(self, db_name):
        if self.user and self.password:
            client = MongoClient('mongodb://{}:{}@{}:{}'.format(
                self.user,
                self.password, 
                self.host, 
                self.port
            ))
        else:
            client = MongoClient(
                self.host,
                port=self.port, 
            )
        db = client[db_name]
        return db