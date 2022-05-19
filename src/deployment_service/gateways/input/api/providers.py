
from fastapi.responses import JSONResponse
from deployment_service.gateways.output.deploy.kubernetes import KubernetesDeploymentOutputGateway
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

router = APIRouter()

@router.get('/providers')
async def providers(user):
    return []

@router.post('/providers')
async def providers(user):
    return []

@router.delete('/providers')
async def providers(user):
    return []

@router.patch('/providers')
async def providers(user):
    return []