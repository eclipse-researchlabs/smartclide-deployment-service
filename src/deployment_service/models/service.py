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
