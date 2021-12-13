from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.postgres.postgre_repo import PostgresRepo
from deployment_service.repositories.postgres.postgres_obj import Base, Deployment

class DeploymentRepository(PostgresRepo):
    def __init__(self, connection_data):
        # connection_string = "postgresql+psycopg2://{}:{}@{}/{}".format(
        #     connection_data["user"],
        #     connection_data["password"],
        #     connection_data["host"],
        #     connection_data["dbname"],
        # )
        self.engine = create_engine()
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def __create_deployment_object(self, results):
        return [
            Deployment(
                username=q.username,
                project_name=q.project_name,
                domain=q.domain,
                port=q.port,
                provider=q.provider,
                services=[],
                replicas=q.replicas,
                status=q.status,
                timestamp=q.timestamp
            )
            for q in results
        ]

    def list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Deployment)

        return self.__create_deployment_object(query.all())


    def save(self, deployment):
        pass