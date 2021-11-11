from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from gitlab.v4.objects import deployments
from deployment_service.gateways.output.gitlab_pipeline import GitlabPipelineOutputGateway
from deployment_service.gateways.output.kubernetes_deployment import KubernetesDeploymentOutputGateway
from deployment_service.use_cases.deployments import create_or_update_deployment
from deployment_service.models.deployment import Deployment
from deployment_service.repositories.postgres.postgre_repo import PostgresRepo
from deployment_service.use_cases.deployments import list_deployments
from fastapi.encoders import jsonable_encoder
from kubernetes.dynamic.exceptions import NotFoundError
import json
from urllib3.exceptions import MaxRetryError

router = APIRouter()

kubernetes_deployment = KubernetesDeploymentOutputGateway()
repo = PostgresRepo({
    'user': 'unicorn_user',
    'password': 'magical_password',
    'host': 'localhost',
    'dbname': 'deployment_service'
})


@router.post('/deploy/')
async def run_deployment(deployment: Deployment):
    try:
        result = create_or_update_deployment(
            repo, kubernetes_deployment, deployment)

        if result == 200:
            return JSONResponse(
                content={'message': 'success'},
                # {
                #     'deployment': {
                #         'name': result.metadata.name,
                #         'namespace': result.metadata.namespace,
                #         'generation': result.metadata.generation,
                #         'container_image': result.spec.template.spec.containers[0].image
                #     }
                # },
                status_code=result.get('code')
            )
        else:
            # Deployment already running
            return JSONResponse(
                content={
                    'message': result.get('message'), 
                    'reason': result.get('reason')
                }, 
                status_code=result.get('code')
            )

    except Exception as ex:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                'message': str(ex)
            },
            status_code=500
        )

# @router.get('/deployments/')
# async def get_deployments(skip: int = 0, limit: int = 10):
#     return JSONResponse(content=list_deployments(repo))


@router.get('/deployments/{id}')
async def get_deployment():
    return []


@router.delete('/deployments/{project_name}')
async def delete_deployment(project_name):
    try:
        result = kubernetes_deployment.delete_deployment(project_name)
        return JSONResponse(content={'message': 'deployment was successfully deleted'}, status_code=200)

    except NotFoundError:
        return JSONResponse(content={'message': 'deployment not found'}, status_code=200)
    except MaxRetryError:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': 'Max retries'}, status_code=200)

    except:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': 'internal server error'}, status_code=500)

