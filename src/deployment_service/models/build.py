#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

from abc import ABCMeta
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
from typing import Optional

@dataclass
class Build():
    id: int
    project: str
    status: str
    image: str = None
    branch: str = None 
    started_at: datetime = None
    finished_at: datetime = None
    duration: float = None
    username: str = None
    avatar_url: str = None
    commit_id: str = None
    commit_msg: str = None
    committer_name: str = None



    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)

    # def __str__(self):
    #     return f'Deployment({self.project}, {self.status}, {self.image}, {self.branch}, {self.started_at}, {self.finished_at}, {self.duration}, {self.username}, {self.avatar_url}, {self.commit_id}, {self.commit_msg}, {self.committer_name})'
