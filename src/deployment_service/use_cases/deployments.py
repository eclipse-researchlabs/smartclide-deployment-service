from deployment_service.gateways.output.mom_output import MOMMQTTOutputGateway
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
        mom_gw = MOMMQTTOutputGateway()
        ret = mom_gw.send_deployment_is_running()
        if ret: return deployment_result
        # result = repo.create_or_update_deployment(deployment)

