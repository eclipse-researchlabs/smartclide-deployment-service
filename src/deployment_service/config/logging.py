#*******************************************************************************
# Copyright (C) 2021-2022 Wellness TechGroup
# 
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
# 
# SPDX-License-Identifier: EPL-2.0
#*******************************************************************************

# -*- coding: utf-8 -*-
import sys
import os.path
import logging
import logging.config

CONFIG_FILE = 'logging.conf'

config_file = None

if os.path.isfile(CONFIG_FILE):
    config_file = CONFIG_FILE

if config_file is not None:
    logging.config.fileConfig(config_file)
    logger = logging.getLogger('deployment-service')
    logger.debug(' - Loading logging config file {} - '.format(config_file))
else:
    # Default logging config
    logging.basicConfig(level=logging.WARN)
    logging.error('- deployment-service - Logging configuration file not found (logging.conf).')
    logger = logging
