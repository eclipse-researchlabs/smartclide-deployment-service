#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

def get_build_status(gateway):
    status = gateway.get_project_build_status()
    return status

def build_project(repo, gateway, branch, ci_file):
    build = gateway.build(
        branch=branch,
        ci_file=ci_file
    )
    return build

def build_list(gateway):
    build_list = gateway.get_builds_list()
    return build_list
