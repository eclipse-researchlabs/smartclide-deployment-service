def list_deployments(repo):
    return repo.list()

def create_or_update_deployment(gateway, image, replicas, hostname, port):    
    deployment_result = gateway.deploy(
            project=image.split('/')[1], 
            image=image, 
            replicas=int(replicas),
            host=hostname, 
            port=int(port)
        )

    if deployment_result:
        return deployment_result
        # result = repo.create_or_update_deployment(deployment)

