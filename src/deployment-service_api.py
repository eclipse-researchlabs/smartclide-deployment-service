#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

import uvicorn
from fastapi import FastAPI
# from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# from deployment_service.config.settings import Settings
# from deployment_service.config.logging import logger as l
from deployment_service.gateways.input.api.metrics import router as metrics_router
from deployment_service.gateways.input.api.deployments import router as deployments_router
from deployment_service.gateways.input.api.builds import router as builds_router
from deployment_service.gateways.input.api.providers import router as providers_router

# settings = Settings()

api = FastAPI(title="SmartCLIDE deployment service API")

# @api.get('/')
# async def root():
#     return JSONResponse(content='SmartCLIDE deployment API', status_code=200)

api.include_router(builds_router)
api.include_router(providers_router)
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

        print(f"[+] Starting Deployment service API on port 3000")
        uvicorn.run(api, host='0.0.0.0', port=3000)
    except Exception as err:
        print(f"[-] Error running SmartCLIDE deployment API': {err}")
