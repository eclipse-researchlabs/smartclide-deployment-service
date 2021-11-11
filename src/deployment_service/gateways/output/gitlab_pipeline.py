import gitlab
from gitlab.cli import docs

from deployment_service.config.settings import Settings
class GitlabPipelineOutputGateway():
    def __init__(self, project_name, username, docker_password):
        settings = Settings()
        self.project_name = project_name
        self.docker_user = username
        self.docker_passwd = docker_password
        self.gl_client = self.__get_gl_client()
        self.project = self.get_current_project(project_name)
        # self.deployments = self.list_project_deployments(self.project)

    def __get_gl_client(self):
        gl = gitlab.Gitlab('https://gitlab.com', private_token='THaukuexsHeVnCqFBZTw')
        return gl

    def get_current_project(self, project_name):
        projects = self.gl_client.projects.list(visibility='private')
        current_project = list(filter(lambda project: project.name == project_name, projects))[0]
        self.token = current_project.triggers.list()[0].token
        return current_project

    def list_project_deployments(self):
        deployments = self.project.deployments.list()
        return deployments

    def build(self):
        result = self.project.trigger_pipeline(
            'master', self.token, 
            variables = {
                "DOCKER_PROJECT": self.project.name,
                "DOCKER_USER": self.docker_user, 
                "DOCKER_PASSWD": self.docker_passwd if self.docker_passwd else 'fake'
            }
        )
        return result
        
    def get_project_build_status(self):
        import pytest
        pytest.set_trace
        status = self.project.jobs.list()[0].status
        return status
