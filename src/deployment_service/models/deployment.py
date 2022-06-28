from abc import ABCMeta
from pydantic.dataclasses import dataclass
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from gitlab.v4.objects import deployments
from deployment_service.models.service import Service
from deployment_service.models.provider import Provider
from typing import List
import uuid

@dataclass
class Deployment():
    id: str
    user: str
    project: str
    domain: str
    port: int
    # provider: Provider
    # services: List[Service]
    replicas: int
    status: str
    k8s_url: str
    created_at: datetime
    stopped_at: datetime


    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)

