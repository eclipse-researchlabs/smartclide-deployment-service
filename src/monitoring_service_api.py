import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from deployment_service.api import deployment
# from deployment_service.config.settings import Settings
# from deployment_service.config.logging import logger as l

# settings = Settings()
api = FastAPI()

api.include_router(deployment.monitoring_router)

    
if __name__ == '__main__':

    try:
        print(f"[+] Starting Monitoring service API on port 3001")
        uvicorn.run(api, host='0.0.0.0', port=3001)
    except Exception as err:
        print(f"[-] Error running Endpoint Manager API: {err}")