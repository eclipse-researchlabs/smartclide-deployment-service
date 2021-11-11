from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Deployment(Base):
    __tablename__ = 'deployment'
    id = Column(Integer, primary_key=True)
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
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name: Column(String(36), nullable=False)
    ipv4: Column(String(15), nullable=False)
    port: Column(Integer, primary_key=False)
    deployment_id = Column(Integer, ForeignKey('deployment.id'))
    deployment = relationship("Deployment")
