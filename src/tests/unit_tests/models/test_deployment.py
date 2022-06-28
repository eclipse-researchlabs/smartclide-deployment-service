from datetime import datetime
from deployment_service.models.deployment import Deployment


deployment_dict = {}

class TestDeploymentModel(object):

    def test_001_deployment_model_constructor(self):
        depl = Deployment(
            _id='',
            user='pberrocal',
            project='test_deployment',
            domain='test.smartclide.eu',
            port=8888,
            replicas=5,
            status='active',
            timestamp=datetime.now()
        )

        deployment_dict = depl.to_dict()

        assert len(depl.to_dict().keys()) == 8

    def test_002_deployment_model_to_dict(self):
        depl = Deployment(
            _id='',
            user='pberrocal',
            project='test_deployment',
            domain='test.smartclide.eu',
            port=8888,
            replicas=5,
            status='active',
            timestamp=datetime.now()
        )

        assert isinstance(depl.to_dict(), dict)
        # import pytest;pytest.set_trace()

    