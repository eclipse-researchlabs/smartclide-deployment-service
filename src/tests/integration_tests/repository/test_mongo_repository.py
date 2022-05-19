from pygit import repos
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.mongo.deployment import MongoDeploymentRepository
from datetime import datetime
import uuid
class TestMongoRepository(object):
    
    def test_000_create_or_update_deployment_obj(self):
        d_dict = Deployment(
            _id='38c66e7b-a7ec-430e-8937-03f43627812b',
            user='pberrocal',
            project='test-kubernetes',
            domain='test.smartclide.eu',
            port=8888,
            replicas=5,
            status='active',
            k8s_url='https://192.168.39.96:8443',
            created_at='2022-05-17T10:16:35.459683',
            stopped_at='2022-05-18T10:16:35.459683'
        ).to_dict()

        repository = MongoDeploymentRepository()
        ret = repository._create_deployment_obj(d_dict)
        assert ret
        
        
    def test_001_create_or_update_deployment(self):
        d_dict = Deployment(
            _id='38c66e7b-a7ec-430e-8937-03f43627812b',
            user='pberrocal',
            project='test-kubernetes',
            domain='test.smartclide.eu',
            port=8888,
            replicas=5,
            status='active',
            k8s_url='https://192.168.39.96:8443',
            created_at='2022-05-17T10:16:35.459683',
            stopped_at='2022-05-18T10:16:35.459683'

        ).to_dict()
        repository = MongoDeploymentRepository()
        ret = repository.create_or_update_deployment(d_dict)
        assert ret


    def test_002_create_or_update_deployment(self):
        ret = None
        for x in range(0, 500):

            d_dict = Deployment(
                _id=str(uuid.uuid4()),
                user='pberrocal',
                project='test-kubernetes',
                domain='test.smartclide.eu',
                port=8888,
                replicas=5,
                status='active',
                k8s_url='https://192.168.39.96:8443',
                created_at='2022-05-17T10:16:35.459683',
                stopped_at='2022-05-18T10:16:35.459683'

            ).to_dict()
        repository = MongoDeploymentRepository()
        ret = repository.create_or_update_deployment(d_dict)
        assert ret

    def test_003_list_deployments(self):
        repository = MongoDeploymentRepository()
        deployments = repository.list_deployments('pberrocal', 'test-kubernetes')
        assert deployments
        assert isinstance(deployments, list)

    def test_004_set_deployment_stopped(self):
        repository = MongoDeploymentRepository()
        result = repository.set_deployment_stopped('56437bf0-ab55-4945-bf7b-f20273b4766e')
        assert result