from abc import ABCMeta
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
from typing import Optional

@dataclass
class Build():
    uuid.UUID
    project: str
    username: Optional[str] = None
    image: Optional[str] = None
    docker_password: Optional[str] = None
    timestamp: Optional[datetime] = None
    tag: Optional[str] = None
    version: Optional[str] = None

