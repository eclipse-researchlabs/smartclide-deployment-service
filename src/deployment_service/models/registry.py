from abc import ABCMeta
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid



@dataclass 
class Registry():
    username: str
    passwd : str
    url: str
