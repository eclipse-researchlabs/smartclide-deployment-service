import urllib.parse
from pymongo import MongoClient
from deployment_service.config.settings import Settings

class MongoRepo:
    def __init__(self, collection_name='deployment_component', page_size=50)-> None:
        settings = Settings()
        self.host = settings.repositories['mongo']['host']
        self.port = int(settings.repositories['mongo']['port'])
        self.user = urllib.parse.quote_plus(settings.repositories['mongo']['user'])
        self.password = urllib.parse.quote_plus(settings.repositories['mongo']['password'])
        self.database = settings.repositories['mongo']['database']
        db = self.__get_mongo_db()
        # select the collection for storing deployments
        self.deployments_col = db[collection_name]

    def __get_mongo_db(self):
        if self.user and self.password:
            client = MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
                self.user,
                self.password,
                self.host,
                self.port,
                self.database
            ))
            # use the database, which this user is allowed to access
            return client[self.database]
        else:
            client = MongoClient(
                self.host,
                port=self.port
            )
            # use the default test database
            return client.test
