from fastapi import APIRouter, Header, Depends, Body
from typing import List, Optional
# from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from deployment_service.models.build import Build
from deployment_service.gateways.output.gitlab_pipeline import GitlabPipelineOutputGateway
from deployment_service.models.build import Build
from deployment_service.use_cases.builds import build_project, get_build_status, build_list

router = APIRouter()


# @router.get('/builds/')
# async def read_builds(skip: int = 0, limit: int = 10, build__name: str = ''):

#     return []
        
@router.get('/builds/')
async def get_builds_list(project: str, x_token: str = Header(None) ):
    gitlab_gw = GitlabPipelineOutputGateway(project, x_token)
    try:
        builds = build_list(gitlab_gw)
        return JSONResponse(content=builds, status_code=200)
    except Exception as ex:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': ex}, status_code=500)

@router.get('/builds/{project}')
async def get_project_latest_build(project: str, x_token: str = Header(None) ):
    try:
        gitlab_gw = GitlabPipelineOutputGateway(project, x_token)
        result = gitlab_gw.get_project_build_status()
        # import pdb
        # pdb.set_trace()
        if result:
            return JSONResponse(result)
        else:
            import pdb
            pdb.set_trace()
            raise Exception('ssssssss')

    except Exception as ex:
        import traceback
        traceback.print_exc()
        JSONResponse(content={
            'message': ex
        })


@router.post('/builds')
async def create_build(
    project: str, 
    x_token: str = Header(None), 
    branch: str = 'master', 
    ci_file: dict = Body(None)):

    try:
        gitlab_gw = GitlabPipelineOutputGateway(project, x_token)
        status = get_build_status(gitlab_gw)
        if status == 'running':
            return JSONResponse(
                content={
                    'status': 'pending',
                    'message': f'Pipeline job {status}'
                }, 
                status_code=200
            )

        else:
            build = build_project(gitlab_gw, branch, ci_file)
            if build:
                return JSONResponse(
                    content=build, 
                    # {
                    #     'state': 'pending',
                    #     'message': f'Pipeline job started',
                    # }, 
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
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                'message': 'Server error: {}'.format(str(ex))
            }, 
            status_code=500)

