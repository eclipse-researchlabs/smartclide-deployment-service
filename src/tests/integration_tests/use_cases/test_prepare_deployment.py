from deployment_service.use_cases.deployments import prepare_deployment

class TestPrepareDeploymentUseCase(object):
    def test_001_prepare_deployment(self):
        ret = prepare_deployment('https://gitlab.dev.smartclide.eu/', 'pberrocal', 'wellness_challenge')
        assert ret