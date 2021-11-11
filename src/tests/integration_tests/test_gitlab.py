import pytest
from deployment_service.config.settings import Settings
from deployment_service.gateways.output.gitlab_pipeline import GitlabPipelineOutputGateway


class TestGitLabPipelineGateway(object):

    def test_001_constructor(self):
        gl = GitlabPipelineOutputGateway('hello-world-node')
        assert gl

    def test_002_get_current_project(self):
        gl = GitlabPipelineOutputGateway('hello-world-node')
        current_project = gl.get_current_project('hello-world-node')
        assert current_project[0].id == 29901293

    def test_003_project_build(self):
        gl = GitlabPipelineOutputGateway('hello-world-node')
        result = gl.build()
        assert result