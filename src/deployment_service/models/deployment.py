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
from pydantic.dataclasses import dataclass
from dataclasses import dataclass, asdict
from datetime import datetime

from gitlab.v4.objects import deployments
from deployment_service.models.service import Service
from deployment_service.models.provider import Provider
from typing import List
import uuid

@dataclass
class Deployment():
    uuid: uuid.UUID
    username: str
    project: str
    domain: str
    port: int
    provider: Provider
    services: List[Service]
    replicas: int
    status: str
    timestamp: datetime


    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)

