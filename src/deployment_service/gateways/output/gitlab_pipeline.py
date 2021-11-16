import gitlab
from gitlab.cli import docs

from deployment_service.config.settings import Settings
from deployment_service.config.logging import logger as l

class GitlabPipelineOutputGateway():
    def __init__(self, project, gitlab_token):
        settings = Settings()
        self.project_name = project
        self.gl_client = self.get_gl_client(gitlab_token)
        self.token = self.gl_client.headers["PRIVATE-TOKEN"]
        self.project = self.get_current_project(self.project_name)
        self.username = self.project.users.list()[0].username

    def get_gl_client(self, private_token):
        try:
            g = gitlab.Gitlab('https://gitlab.com', private_token=private_token)
            return g
        except gitlab.exceptions.GitlabHttpError as he:
            if str(he) == "401 Unauthorized":
                return None, False
            else:
                l.debug(f"Unexpected error getting authorization token (Reason: {str(he)})")

    def get_current_project(self, project):
        projects = self.gl_client.projects.list(visibility='private')
        current_project = list(filter(lambda p: p.name == project, projects))[0]
        self.token = current_project.triggers.list()[0].token
        return current_project

    def list_project_deployments(self):
        deployments = self.project.deployments.list()
        return deployments

    def build(self):
        result = self.project.trigger_pipeline(
            'master', self.token, 
            # variables = {
            #     "DOCKER_PROJECT": self.project_name,
            #     "DOCKER_USER": self.username, 
            #     "DOCKER_PASSWD": 'fake'
            # }
        )
        return self.get_project_build_status()
        
    def get_project_build_status(self):
        status = self.project.jobs.list()[0].status
        user = self.project.pipelines.list()[0].variables.list()[2].attributes['value']
        project = self.project.pipelines.list()[0].variables.list()[1].attributes['value']
        return {
            'status': status,
            'image': f'{user}/{project}',  
            'job': self.project.jobs.list()[0].attributes
        }
