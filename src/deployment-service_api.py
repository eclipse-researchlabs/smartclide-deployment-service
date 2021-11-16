import uvicorn
from fastapi import FastAPI
# from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from deployment_service.api import deployment, build, monitoring
# from deployment_service.config.settings import Settings
# from deployment_service.config.logging import logger as l
from deployment_service.api.monitoring import router as monitoring_router
from deployment_service.api.deployment import router as deployment_router
from deployment_service.api.build import router as build_router
# settings = Settings()

api = FastAPI(title="SmartCLIDE deployment service API")

# @api.get('/')
# async def root():
#     return JSONResponse(content='SmartCLIDE deployment API', status_code=200)

api.include_router(build_router)
api.include_router(deployment_router)
api.include_router(monitoring_router)

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

        print(f"[+] Starting Deployment service API on port 3000")
        uvicorn.run(api, host='0.0.0.0', port=3000)
    except Exception as err:
        print(f"[-] Error running SmartCLIDE deployment API': {err}")