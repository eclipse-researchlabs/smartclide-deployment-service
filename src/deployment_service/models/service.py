from abc import ABCMeta
from dataclasses import dataclass, asdict
from datetime import datetime
from dataclasses import dataclass, asdict

from deployment_service.models.build import Build

@dataclass
class Service():
    # build: Build
    name: str
    ipv4: str
    port: int

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)