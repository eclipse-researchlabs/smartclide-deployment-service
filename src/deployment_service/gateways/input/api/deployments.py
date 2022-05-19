from kubernetes.dynamic.exceptions import NotFoundError, ApiException
from urllib3.exceptions import MaxRetryError
from fastapi import APIRouter, Query, Header
from typing import Optional
from fastapi.responses import JSONResponse
from deployment_service.gateways.output.deploy.kubernetes import KubernetesDeploymentOutputGateway
from deployment_service.repositories.mongo.deployment import MongoDeploymentRepository
from deployment_service.use_cases.deployments import create_or_update_deployment, get_deployments_list
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.postgres.postgre_repo import PostgresRepo
from deployment_service.config.settings import Settings

settings = Settings()
router = APIRouter()
mongo_repo = MongoDeploymentRepository()

@router.get('/deployments/')
async def list_deployments(
    user: str,
    project: str, 
    skip: int = 0, 
    limit: int = 10):

    try:
        deployments = mongo_repo.list_deployments(user, project, skip, limit)
        if not deployments:
            return JSONResponse(content={'message': 'Deployments not found'}, status_code=404)
        else:
            return JSONResponse(content=deployments, status_code=200)
    
    except Exception as ex:
        import traceback; traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'}, status_code=500)


@router.get('/deployments/{id}')
async def read_deployment(id: str, k8s_token: str = Header(None)):

    try:    
        deployment = mongo_repo.show_deployment(id)
        if deployment:
            kubernetes_gw = KubernetesDeploymentOutputGateway(deployment['k8s_url'], k8s_token)
            status = kubernetes_gw.deployment_status(deployment['project'])

            if not status:
                return JSONResponse(content={'message': 'Deployment not running'}, status_code=404)
            else:
                return JSONResponse(content=deployment, status_code=200)
        
    except Exception as ex:
        import traceback; traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'}, status_code=500)


@router.post('/deployments/')
async def run_deployment(
    user: str,
    git_repo_url: str,
    project_name: str,
    k8s_url: str,
    hostname: str,
    k8s_token: str = Header(None), 
    gitlab_token: str = Header(None),
    branch: Optional[str] = 'master',
    replicas: Optional[int] = 1,
    deployment_port: int = 80):
    
    try:
        result = create_or_update_deployment(k8s_url, k8s_token, project_name, user, deployment_port, replicas, hostname)
        if result:
            return JSONResponse(content = result,status_code = 200 )
        else:
            return JSONResponse(content={'message': 'Deployment already running'}, status_code=409)

    except Exception as ex:
        import traceback; traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'},status_code=500)


@router.delete('/deployments/{id}')
async def delete_deployment(id: str, k8s_token: str = Header(None)):

    try:
        deployment = mongo_repo.show_deployment(id)
        kubernetes_gw = KubernetesDeploymentOutputGateway(deployment['k8s_url'], k8s_token)
        stopped_deployment = mongo_repo.set_deployment_stopped(id)
        result = kubernetes_gw.stop(deployment['project'])
        if result:
            return JSONResponse(content=stopped_deployment, status_code=200)
        else:
            return JSONResponse(content={'message': 'Deployment not running'}, status_code=404)    
    except (NotFoundError, ApiException):
        return JSONResponse(content={'message': 'Deployment not found'}, status_code=404)
    except MaxRetryError:
        return JSONResponse(content={'message': 'Max retries'}, status_code=500)
    except Exception as ex:
        import traceback; traceback.print_exc()
        return JSONResponse(content={'message': f'Internal server error: {ex}'}, status_code=500)
