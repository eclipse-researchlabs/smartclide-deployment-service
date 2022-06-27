#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

from fastapi.responses import JSONResponse
from deployment_service.gateways.output.kubernetes_deployment import KubernetesDeploymentOutputGateway
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
