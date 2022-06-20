import pytest
from deployment_service.config.settings import Settings
from deployment_service.gateways.output.build.gitlab import GitlabPipelineOutputGateway


class TestGitLabPipelineGateway(object):

    def test_001_constructor(self):
        gl = GitlabPipelineOutputGateway('test-kubernetes', 'oEFB82mtzww5S7-JA2n9')
        assert gl

    def test_002_get_current_project(self):
        gl = GitlabPipelineOutputGateway('test-kubernetes', 'oEFB82mtzww5S7-JA2n9')
        current_project = gl.get_current_project('test-kubernetes')
        assert current_project.id == 18

    def test_003_project_build(self):
        gl = GitlabPipelineOutputGateway('test-kubernetes', 'oEFB82mtzww5S7-JA2n9')
        result = gl.build('develop', {})
        assert result