from sqlalchemy.orm import sessionmaker
from deployment_service.models.build import Build
from deployment_service.repositories.mongo.mongo_repository import MongoRepo
from deployment_service.repositories.postgres.postgres_obj import Build

class BuildRepository(MongoRepo):

    def __init__(self):
        self.db = self.get_mongo_client().builds

    def __create_deployment_object(self, results):
        return [
            Build(
                id=q['id'],
                project=q['project'],
                status=q['status'],
                image=q['image'],
                branch=q['branch'], 
                started_at=q['started_at'],
                finished_at=q['finished_at'],
                duration=q['duration'],
                username=q['username'],
                avatar_url=q['avatar_url'],
                commit_id=q['commit_id'],
                commit_msg=q['commit_msg'],
                committer_name=q['commiter_name']
            )
            for q in results
        ]

    def list(self, filters=None):
        results = self.db.persons.find({}) 
        return [
            self.__create_deployment_object(q).to_dict() for q in results
        ]


    def save(self, build):
        try:
            result = self.db.builds.insert_one(build)
            return True
        except:
            import pdb
            pdb.set_trace()
            # return self.__create_deployment_object([result])