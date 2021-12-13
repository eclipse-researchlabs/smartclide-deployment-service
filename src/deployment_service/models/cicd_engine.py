from abc import ABCMeta
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class CICDEngine():
    name: str 
    