from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.postgres.postgres_obj import Base, Deployment

class PostgresRepo:
    def __init__(self, 
        user: str ='unicorn_user', 
        password: str ='magical_password', 
        host: str ='localhost', 
        dbname: str ='rainbow_database'
    ):
        connection_string = 'postgresql+psycopg2://unicorn_user:magical_password@localhost/rainbow_database'
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
