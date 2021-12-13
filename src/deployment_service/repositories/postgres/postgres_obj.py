import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class Deployment(Base):
    __tablename__ = 'deployments'
    id = Column(Integer, primary_key=True, default=uuid.uuid4)
    timestamp = Column(Time, nullable=False)
    status = Column(String(36), nullable=False)
    project_name = Column(String(36), nullable=False)
    username: Column(String(36), nullable=False)
    domain: Column(String(36), nullable=False)
    port: Column(Integer, primary_key=False)
    provider_id: Column(Integer, ForeignKey('provider.id'))
    services: relationship("Service", cascade="all, delete")
    replicas: Column(Integer, primary_key=False)


class Service(Base):
    __tablename__ = 'services'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Column(String(36), nullable=False)
    ipv4: Column(String(15), nullable=False)
    port: Column(Integer, primary_key=False)
    deployment_id = Column(Integer, ForeignKey('deployments.id'))
    deployment = relationship("Deployment")

class Build(Base):
    __tablename__ = 'builds'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project: Column(String(36), nullable=False)
    service: Column(String(36), nullable=False)
    image: Column(String(36), nullable=False)
    branch: Column(String(36), nullable=False)
    started_at: Column(DateTime, nullable=False)
    finished_at: Column(DateTime, nullable=False)
    duration: Column(Float, nullable=False)
    username: Column(String(36), nullable=False)
    avatar_url: Column(String(36), nullable=False)
    commit_id: Column(Integer, nullable=False)
    commit_msg: Column(String(36), nullable=False)
    committer_name: Column(String(36), nullable=False)

