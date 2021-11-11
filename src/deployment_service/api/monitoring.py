
from fastapi.responses import JSONResponse
from deployment_service.gateways.output.kubernetes_deployment import KubernetesDeploymentOutputGateway
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

router = APIRouter()

@router.get('/monitoring/{user}/{project_name}')
async def monitoring(user, project_name):
    try:
        deployment = KubernetesDeploymentOutputGateway()
        # import pytest
        # pytest.set_trace()
        deployment_status = deployment.deployment_status(project_name)
        json_compatible_item_data = jsonable_encoder(deployment_status)
        return JSONResponse(content=json_compatible_item_data, status_code=200)
        # return JSONResponse(content={}, status_code=200)
    except Exception as ex:
        return JSONResponse(content={'message': 'deployment not found'}, status_code=404)
    except:
        return JSONResponse(content={'message': 'internal server error'}, status_code=500)