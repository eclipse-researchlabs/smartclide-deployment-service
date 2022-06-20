
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from deployment_service.gateways.output.deploy.kubernetes import KubernetesDeploymentOutputGateway
from deployment_service.repositories.mongo.deployment import MongoDeploymentRepository


router = APIRouter()
mongo_repo = MongoDeploymentRepository()

@router.get('/metrics/{id}')
async def metrics(id: str, k8s_token: str = Header(None)):
    
    try:
        deployment = mongo_repo.show_deployment(id)
        k_gw = KubernetesDeploymentOutputGateway(deployment['k8s_url'], k8s_token)
        container_metrics = k_gw.get_deployment_metrics(deployment['project'], deployment['k8s_url'])
        if container_metrics:
            return JSONResponse(content=container_metrics, status_code=200)
        else:
             return JSONResponse(content={'message': 'deployment not running'}, status_code=404)

    except Exception as ex:
        import traceback; traceback.print_exc()
        return JSONResponse(content={'message': str(ex)}, status_code=500)