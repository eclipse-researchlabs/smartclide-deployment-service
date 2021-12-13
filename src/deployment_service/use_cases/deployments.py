def get_deployments_list(gateway):
    return gateway.list_deployments()

def create_or_update_deployment(gateway, image, replicas, hostname, port):    
    deployment_result = gateway.deploy(
            project=image.split('/')[1], 
            image=image, 
            replicas=int(replicas),
            host=hostname, 
            port=int(port)
        )

    if deployment_result:
        # result = repo.create_or_update_deployment(deployment)
        return deployment_result

