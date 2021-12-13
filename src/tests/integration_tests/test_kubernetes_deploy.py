from re import S
import pytest
from deployment_service.config.settings import Settings
from deployment_service.gateways.output.kubernetes_deployment import KubernetesDeploymentOutputGateway


class TestGitLabPipelineGateway(object):

    def test_001_constructor(self):
        kd = KubernetesDeploymentOutputGateway()
        assert kd

    def test_002_deploy(self):
        kd = KubernetesDeploymentOutputGateway()
        result = kd.deploy(project_name='test-kubernetes', image='pberrocal/test-kubernetes', replicas=1, host='testkubernetes.com', port=80)
        pytest.set_trace()
        assert result

    def test_003_service_status(self):
        kd = KubernetesDeploymentOutputGateway()
        status = kd.deployment_status('hello-world-node')
        assert isinstance(status, dict)
