import uvicorn
from fastapi import FastAPI
# from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# from deployment_service.config.settings import Settings
from deployment_service.config.logging import logger as l
from deployment_service.gateways.input.api.metrics import router as metrics_router
from deployment_service.gateways.input.api.deployments import router as deployments_router
from deployment_service.gateways.input.api.builds import router as builds_router
from deployment_service.gateways.input.api.providers import router as providers_router

# settings = Settings()
host = '0.0.0.0'
port = 3000
api = FastAPI(title="SmartCLIDE deployment component API")
# api.include_router(builds_router)
# api.include_router(providers_router)
api.include_router(deployments_router)
api.include_router(metrics_router)

origins = ['*']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    try:
        print(f"\n[INFO] Starting Deployment service API on  {host}:{port}")
        uvicorn.run(api, host=host, port=port)
    except Exception as err:
        print(f"[ERROR] Error running SmartCLIDE deployment API': {err}")