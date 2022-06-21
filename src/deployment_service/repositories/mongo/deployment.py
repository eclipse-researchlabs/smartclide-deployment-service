import uuid
from datetime import datetime
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.mongo.mongo_repository import MongoRepo

class MongoDeploymentRepository(MongoRepo):

    def _create_deployment_obj(self, deployment: dict) -> Deployment:
        return Deployment(
            id=str(deployment['_id']),
            user=deployment['user'],
            project=deployment['project'],
            domain=deployment['domain'],
            port=deployment['port'],
            # provider: Provider
            # services: List[Service]
            replicas=deployment['replicas'],
            status=deployment['status'],
            k8s_url=deployment['k8s_url'],
            created_at=deployment['created_at'], 
            stopped_at=deployment['stopped_at']
        )

    def create_or_update_deployment(self, deployment: dict) -> bool:
        try:
            deployment_obj =  self._create_deployment_obj(deployment)
            query = {'id': deployment_obj.id} 

            rc = self.deployments_db.update(query, deployment_obj.to_dict(), True)
            if rc:
                return deployment_obj

        except Exception as ex:
            print('{}: Failed to update or create deployment'.format(ex))
            return False


    def create_deployment_objects(self, results: list) -> list:
        return [self._create_deployment_obj(q).to_dict() for q in results]

        
    def list_deployments(self, user, project, skip: int = 0, limit: int=20) -> list:
        filter = {'user': user, 'project': project}
        try:
            count = self.deployments_db.find().count()
            deployments = self.deployments_db.find(filter).limit(limit).skip(skip).sort('timestamp',-1)
            return {
                'data': self.create_deployment_objects(deployments),
                'count': count
            }
        except:
            import traceback; traceback.print_exc()

    def show_deployment(self, id):
        try:
            deployments = self.deployments_db.find({"_id": id}).limit(1)
            if deployments:
                return self.create_deployment_objects(deployments)[0]
        except:
            import traceback; traceback.print_exc()

    def set_deployment_stopped(self, id):
        try:
            deployments = self.deployments_db.find({"_id": id}).limit(1)
            if deployments:
                deployment = self.create_deployment_objects(deployments)[0]
                deployment['status'] = 'stopped'
                deployment['stopped_at'] = datetime.now().isoformat()
                stopped_deployment = self.create_or_update_deployment(deployment)
                return stopped_deployment
        except:
            import traceback; traceback.print_exc()