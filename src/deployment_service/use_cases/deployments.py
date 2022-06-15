import uuid
from datetime import datetime
from deployment_service.gateways.output.mom.amqp import MOMAMQPOutputGateway
from deployment_service.repositories.mongo.deployment import MongoDeploymentRepository
from deployment_service.gateways.output.deploy.kubernetes import KubernetesDeploymentOutputGateway

def get_deployments_list(gateway):
    return gateway.list_deployments()

def create_or_update_deployment(k8s_url, k8s_token, name, username, port, replicas, hostname):   
    k_gw = KubernetesDeploymentOutputGateway(k8s_url, k8s_token) 
    deployment_result = k_gw.run(
            name=name, 
            image=f'{username}/{name}', 
            replicas=int(replicas),
            host=hostname, 
            port=int(port)
        )
    if deployment_result:
        repo = MongoDeploymentRepository()
        id = str(uuid.uuid4())
        deployment = repo.create_or_update_deployment(
            {
                '_id': id,
                'user': username,
                'project': name,
                'domain': hostname,
                'port': port,
                'replicas': replicas,
                'status': 'active',
                'k8s_url': k8s_url,
                'created_at': datetime.now().isoformat(),
                'stopped_at': ''
            }
        )

        if deployment:
            mom_gw = MOMAMQPOutputGateway()
            ret = mom_gw.send_deployment_is_running(name, id)
            if ret: return deployment.to_dict()
