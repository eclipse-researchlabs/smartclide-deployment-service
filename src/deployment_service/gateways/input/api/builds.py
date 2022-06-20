from fastapi import APIRouter, Header, Depends, Body
from fastapi.responses import FileResponse

from typing import List, Optional
# from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import unquote, urlparse

from deployment_service.models.build import Build
from deployment_service.gateways.output.deploy import GitlabPipelineOutputGateway
from deployment_service.models.build import Build
from deployment_service.use_cases.builds import build_project, get_build_status, build_list
from deployment_service.repositories.mongo.build import BuildRepository
from deployment_service.gateways.input.git.git_input import GitInputGateway
from deployment_service.config.logging import logger as l

router = APIRouter()
        
@router.get('/builds/')
async def get_builds_list(project: str, gitlab_token: str = Header(None) ):
    try:
        # project = urlparse(project_url).path[1:]
        gitlab_gw = GitlabPipelineOutputGateway(project, gitlab_token)
        builds = build_list(gitlab_gw)
        return JSONResponse(content=builds, status_code=200)
    except Exception as ex:
        l.error(f'Error: {ex}')
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'message': ex}, status_code=500)

@router.get('/builds/{project}')
async def get_project_latest_build(project: str, gitlab_token: str = Header(None) ):
    try:
        gitlab_gw = GitlabPipelineOutputGateway(project, gitlab_token)
        result = gitlab_gw.get_project_build_status()
        
        if result:
            return JSONResponse(result)
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
        JSONResponse(content={
            'message': ex
        })


@router.post('/builds')
async def create_build(
    project: str, 
    gitlab_token: str = Header(None), 
    branch: str = 'master', 
    ci_file: dict = Body(None)):

    try:
        # project = urlparse(project_url).path[1:]
        gitlab_gw = GitlabPipelineOutputGateway(project, gitlab_token)
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
            repository = BuildRepository()
            build = build_project(repository, gitlab_gw, branch, ci_file)
            if build:
                return JSONResponse(content=build, status_code=200)

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

@router.get('/builds/ci-cd-file/{project_name}')
async def get_ci_cd_file(project_name: str):
    try:
        git_gw = GitInputGateway()
        fpath = git_gw.write_cdci_file(f'/tmp/repos/{project_name}')
        
        if fpath:
            return FileResponse(fpath, filename='gitlab-ci.yml')
        else:
                return JSONResponse(
                    content={
                        'message': f'Failed to create CI/CD file for project {project_name}'    
                    },
                    status_code=500
                )

    except Exception as ex:
        import traceback
        traceback.print_exc()
        JSONResponse(content={
            'message': ex
        })