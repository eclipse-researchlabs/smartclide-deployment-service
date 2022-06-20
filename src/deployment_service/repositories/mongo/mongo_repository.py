import pymongo

class MongoRepo:
    host: str = 'localhost'
    port: int = 27017

    def __init__(self, host='localhost', port=27017, db_name='deployment_component', page_size=50 )-> None:
        db = self.__get_mongo_client(db_name)
        self.deployments_db = db.deployments
        # import pdb;pdb.set_trace()

    def __get_mongo_client(self, db_name):
        client = pymongo.MongoClient(
            self.host,
            port=self.port, 
        )
        db = client[db_name]
        return db