import pymongo

class MongoRepo:
    host: str = 'localhost'
    port: int = 27017


    def get_mongo_client(self):

        return pymongo.MongoClient(
            self.host,
            port=self.port, 
            # username=self.username, 
            # password=self.password,
            # authSource='deployment_service',
            # authMechanism='SCRAM-SHA-1'
        )
        
        