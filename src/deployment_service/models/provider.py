from abc import ABCMeta
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class Provider():
    uuid.UUID
    provider_name: str
    username: str
    