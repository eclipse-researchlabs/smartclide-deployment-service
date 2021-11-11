def list_deployments(repo):
    return repo.list()

def create_or_update_deployment(repo, gateway, deployment):    
    deployment_result = gateway.deploy(
            project=deployment.project, 
            image='{}/{}'.format(deployment.username, deployment.project), 
            replicas=int(deployment.replicas),
            host=deployment.domain, 
            port=int(deployment.port)
        )

    if deployment_result:
        return deployment_result
        # result = repo.create_or_update_deployment(deployment)

