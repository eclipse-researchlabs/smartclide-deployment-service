from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from gitlab.v4.objects import deployments
from deployment_service.models.build import Build
from deployment_service.gateways.output.gitlab_pipeline import GitlabPipelineOutputGateway
from deployment_service.gateways.output.kubernetes_deployment import KubernetesDeploymentOutputGateway
from deployment_service.models.build import Build
from fastapi.encoders import jsonable_encoder
from kubernetes.dynamic.exceptions import NotFoundError

router = APIRouter()



# @router.get('/builds/')
# async def read_builds(skip: int = 0, limit: int = 10, build__name: str = ''):

#     return []

# @router.get('/builds/{id}')
# async def read_build():
#     return []

@router.post('/build/')
async def create_build(build: Build):
    try:
        gitlab_build = GitlabPipelineOutputGateway(build.project_name, build.username, build.docker_password)
        status = gitlab_build.get_project_build_status()
        
        if status == 'success':
            return JSONResponse(
                content={
                    'status': 'done',
                    'message': f'Pipeline job started',
                }, 
                status_code=200
            )

        if status != 'running':
            result = gitlab_build.build()
            if result:
                return JSONResponse(
                    content={
                        'status': 'pending',
                        'message': f'Pipeline job started',
                    }, 
                    status_code=200
                )

            else:
                return JSONResponse(
                    content={
                        'status': '',
                        'message': 'project {}/{} not found'.format(build.user, build.project_name)    
                    },
                    status_code=400
                )
        else:
            return JSONResponse(
                content={
                    'status': 'pending',
                    'message': f'Pipeline job{status}'
                }, 
                status_code=200
            )
        
    except Exception as ex:
        return JSONResponse(content='Server error: {}'.format(str(ex)), status_code=500)

