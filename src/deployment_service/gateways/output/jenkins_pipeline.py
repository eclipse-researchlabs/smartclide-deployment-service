#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

from api4jenkins import Jenkins
import time
from deployment_service.config.logging import logger as l


class JenkinsOutputGateway(object):

    def __init__(self, url, user, password):
        self.jenkins_client = self.__get_jenkins_client(url, user, password) 
        self.version = self.__get_version()

    def create_job(self, name, config):
        result = self.jenkins_client.create_job(name, config)
        return result
    
    def get_jon(self, name):
        return self.jenkins_client.get_job(name)

    def build_job(self, job_name):
        job = self.jenkins_client.get_job(job_name)
        item = job.build()
        while not item.get_build():
            time.sleep(1)
        build = item.get_build()
        for line in build.progressive_output():
            l.info(line)       
        return build

    def get_build_info(self, name):
        last_build_number = self.jenkins_client.get_job_info(name)['lastCompletedBuild']['number']
        build_info = self.jenkins_client.get_build_info(name, last_build_number)
        return build_info

    def __get_jenkins_client(self, url, user, password):
        j = Jenkins(url, auth=(user, password))
        return j

    def __get_version(self):
        return self.jenkins_client.version
