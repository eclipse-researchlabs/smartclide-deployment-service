#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

import pymongo

class MongoRepo:
    host: str = 'localhost'
    port: int = 27017


    def get_mongo_client(self):

        return pymongo.MongoClient(
            self.host,
            port=self.port, 
        )
        
        
