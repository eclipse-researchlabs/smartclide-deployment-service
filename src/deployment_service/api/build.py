from fastapi import APIRouter, Header, Depends
from typing import List, Optional
# from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from deployment_service.models.build import Build
from deployment_service.gateways.output.gitlab_pipeline import GitlabPipelineOutputGateway
from deployment_service.models.build import Build


router = APIRouter()


# @router.get('/builds/')
# async def read_builds(skip: int = 0, limit: int = 10, build__name: str = ''):

#     return []

# @router.get('/builds/{id}')
# async def read_build():
#     return []
# class BuildRequest(BaseModel):
#     project: str = 'test-kubernetes'
#     gitlab_username: str = 'pberr'
#     gitlab_password: str = 'alg0ritm0'
#     registry_username: str = 'pberrocal'
#     registry_password: str = 'alg0ritm0'

@router.post('/build')
async def create_build(project: str='test-kubernetes', x_token: Optional[str] = Header('glpat-LSc_Qx8z6cGyJtFndYeG')):
    try:
        gitlab_build = GitlabPipelineOutputGateway(project, x_token)
        
        status = gitlab_build.get_project_build_status()
        if status == 'running':
            return JSONResponse(
                content={
                    'status': 'pending',
                    'message': f'Pipeline job {status}'
                }, 
                status_code=200
            )

        else:
            result = gitlab_build.build()
            if result:
                return JSONResponse(
                    content={
                        'state': 'pending',
                        'message': f'Pipeline job started',
                    }, 
                    status_code=200
                )

            else:
                return JSONResponse(
                    content={
                        'state': '',
                        'message': f'Project {project} not found'    
                    },
                    status_code=400
                )
        
    except Exception as ex:
        return JSONResponse(content='Server error: {}'.format(str(ex)), status_code=500)

@router.get('/build')
async def get_build(project, x_token: str = Header('glpat-LSc_Qx8z6cGyJtFndYeG') ):
    try:
        gitlab_build = GitlabPipelineOutputGateway(project, x_token)
        result = gitlab_build.get_project_build_status()
        return JSONResponse(result)
    except Exception as ex:
        import traceback
        traceback.print_exc()
        JSONResponse(content={
            'message': ex
        })