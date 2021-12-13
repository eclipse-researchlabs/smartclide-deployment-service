import pytest
from deployment_service.config.settings import Settings
from deployment_service.gateways.output.jenkins_pipeline import JenkinsOutputGateway

class TestJenkins(object):

    def test_001_job_config(self):
        settings = Settings()
        config = settings.get_job_config('Test02', 'https://github.com/pedbermar/wellness_challenge', 'asd')
        # assert 'Test02' in config
        assert config

    def test_002_get_version(self):
        jenkins = JenkinsOutputGateway(url='http://localhost:8081', user='pberrocal', password='j3nk1n$')
        version = jenkins.version
        assert version == '2.303.1'
    
    def test_003_create_job(self):
        name = 'assets-manager'
        settings = Settings()
        job_config = settings.get_job_config(name, 'https://github.com/pedbermar/wellness_challenge', 'asd')
        # pytest.set_trace()
        jenkins = JenkinsOutputGateway(url='http://localhost:8081', user='pberrocal', password='j3nk1n$')
        job_result = jenkins.create_job(name, job_config)
        result = jenkins.build_job('assets-manager')
        # build_info = jenkins.get_build_info('test_job_004')
        # print(build_info)
        assert result