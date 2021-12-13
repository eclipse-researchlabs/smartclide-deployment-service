from kubernetes.dynamic.exceptions import NotFoundError
from urllib3.exceptions import MaxRetryError
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from deployment_service.gateways.output.kubernetes_deployment import KubernetesDeploymentOutputGateway
from deployment_service.use_cases.deployments import create_or_update_deployment, get_deployments_list
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.postgres.postgre_repo import PostgresRepo

router = APIRouter()
kubernetes_gw = KubernetesDeploymentOutputGateway()

@router.post('/deployments')
async def run_deployment(
    image: str = 'pberrocal/test-kubernetes', 
    hostname: str = 'test-smartclide.net', 
    port: int = 8080, 
    replicas: int = 1):

    try:
        result = create_or_update_deployment(kubernetes_gw, image, replicas, hostname, port)
        if result.get('code') == 200:
            return JSONResponse(
                content={'message': result.get('message')},
                status_code=200)
        else:
            return JSONResponse(
                content={
                    'message': result.get('message'), 
                    'reason': result.get('reason')
                }, 
                status_code=result.get('code'))

    except Exception as ex:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'},status_code=500)


@router.get('/deployments')
async def read_deployment(project):
    try:
        deployment = kubernetes_gw.deployment_status(project)
        if deployment.status == 404:
            return JSONResponse(content={'message': 'Deployment not found'}, status_code=400)
        else:
            message = deployment['conditions'][-1]['message']
            return JSONResponse(content={'message': message}, status_code=200)
    
    except Exception as ex:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'}, status_code=500)

    
@router.get('/deployments/')
async def list_deployments(skip: int = 0, limit: int = 10):
    try:
        deployments = get_deployments_list(kubernetes_gw)
        if not deployments:
            return JSONResponse(content={'message': 'Deployment not found'}, status_code=400)
        else:
            return JSONResponse(content={'message': deployments}, status_code=200)
    
    except Exception as ex:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'}, status_code=500)

@router.delete('/deployments')
async def delete_deployment(project):
    try:
        result = kubernetes_gw.delete_deployment(project)
        return JSONResponse(content={'message': 'Deployment was successfully deleted'}, status_code=200)
    except NotFoundError:
        return JSONResponse(content={'message': 'Deployment not found'}, status_code=400)
    except MaxRetryError:
        return JSONResponse(content={'message': 'Max retries'}, status_code=200)
    except Exception as ex:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'}, status_code=500)

