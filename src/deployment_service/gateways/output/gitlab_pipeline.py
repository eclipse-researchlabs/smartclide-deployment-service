#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

import gitlab

from deployment_service.config.settings import Settings
from deployment_service.config.logging import logger as l
from deployment_service.models.build import Build

class GitlabPipelineOutputGateway():
    def __init__(self, project: str, gitlab_token: str):
        self.settings = Settings()
        self.project_name = project
        self.gl_client = self.get_gl_client(gitlab_token)
        self.token = gitlab_token #self.gl_client.headers["PRIVATE-TOKEN"]
        self.project = self.get_current_project(self.project_name)
        self.username = self.project.users.list()[0].username

    def get_gl_client(self, private_token):
        try:
            url = self.settings.gitlab.get('url')
            client = gitlab.Gitlab(url, private_token=private_token)
            return client
        except gitlab.exceptions.GitlabCreateError as ce:
            l.error(ce)
            return ce
        except gitlab.exceptions.GitlabHttpError as he:
            if str(he) == "401 Unauthorized":
                return None, False
            else:
                l.error(f"Unexpected error getting authorization token (Reason: {str(he)})")

    def get_current_project(self, project):
        projects = self.gl_client.projects.list(visibility='private')
        current_project = list(filter(lambda p: p.name == project, projects))[0]
        # self.token = current_project.triggers.list()[0].token
        return current_project

    # def list_project_deployments(self):
    #     deployments = self.project.deployments.list()
    #     return deployments


    def get_or_create_trigger(self, project):
        trigger_decription = 'my_trigger_id'
        for t in project.triggers.list():
            if t.description == trigger_decription:
                return t
        return project.triggers.create({'description': trigger_decription})

    def build(self, branch: str, ci_file: dict):
        project = self.get_current_project(self.project_name)
        try:
            f = project.files.get(file_path='.gitlab-ci.yml', ref=branch)
        except:
            user_id = self.project.users.list()[0].get_id()
            email = self.gl_client.users.get(user_id).public_email
            f = project.files.create({
                'file_path': 'gitlab-ci.yml',
                'branch': branch,
                'content': ci_file,
                'author_email': email,
                'author_name': self.username,
                'encoding': 'text',
                'commit_message': 'Create .gitlab-ci.yml file'})
            pass
        if f:
            trigger = self.get_or_create_trigger(self.project)
            # variables = {'CI_JOB_TOKEN': trigger.token}
            # variables = {
            #     'IMAGE_NAME': f'{self.repo_owner}/{self.project_name}',
            #     # 'DOCKER_HOST': 'tcp://docker:2375'
            # }
            result = self.project.trigger_pipeline(branch, trigger.token) #, variables=variables)
            if result:
                return self.get_project_build_status()
            else: return False
        else: return False

    def get_project_build_status(self):
        status = self.project.jobs.list()[0].status
        user = self.project.users.list()[0].username
        project = self.project_name
        return self.get_single_build_obj({
            'status': status,
            'image': f'{user}/{project}',  
            'job': self.project.jobs.list()[0].attributes
        }).to_dict()

    def get_builds_list(self):
        results = []
        project = self.project_name
        for job in self.project.jobs.list():
            # import pdb
            # pdb.set_trace()
            status = job.status
            user = job.user['username']
            results.append({
                'status': status,
                'image': f'{self.repo_owner}/{project}',  
                'job': job.attributes
            })
        return self.create_build_objects(results)

    def get_single_build_obj(self, build):
        return Build(
            id=build['job']['id'],
            project=build['image'].split('/')[1], 
            status=build['job']['status'],
            image=build['image'], 
            branch=build['job']['ref'], 
            started_at=build['job']['started_at'], 
            finished_at=build['job']['finished_at'], 
            duration=build['job']['duration'], 
            username=build['job']['user']['username'], 
            avatar_url=build['job']['user']['avatar_url'],
            commit_id=build['job']['commit']['id'], 
            commit_msg=build['job']['commit']['message'], 
            committer_name=build['job']['commit']['committer_name']
        )

    def create_build_objects(self, results: list):
        return [
            self.get_single_build_obj(q).to_dict()
            for q in results
        ]
