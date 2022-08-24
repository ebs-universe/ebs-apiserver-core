# Copyright (C) 2022 Chintalagiri Shashank
# Copyright (C) 2019 Chintalagiri Shashank (tendril-config)
#
# This file is part of EBS API Hub.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Core Configuration Constants
============================
"""

import os

from tendril.utils.config import ConfigConstant

import logging
logger = logging.getLogger(__name__)

depends = []


config_constants_environment = [
    ConfigConstant(
        'ALLOW_ENVIRONMENT_OVERRIDES',
        "True",
        'Whether config options can be overridden from the environment.'
    ),
    ConfigConstant(
        'ENVIRONMENT_OVERRIDE_PREFIX',
        "'{}_'.format(APPNAME.upper())",
        'Environment variable name prefix.'
    ),
]


config_constants_basic = [
    ConfigConstant(
        'INSTANCE_ROOT',
        "os.path.join(os.path.expanduser('~'), '.config', APPNAME)",
        "Path to the EBS API Server instance root. Can be redirected "
        "if necessary with a file named ``redirect`` in this folder."
    )
]


config_constants_redirected = [
    ConfigConstant(
        'INSTANCE_CONFIG_FILE',
        "os.path.join(INSTANCE_ROOT, 'config.py')",
        'Path to the EBS API Server instance configuration.'
    ),
    ConfigConstant(
        'LOCAL_CONFIG_FILE',
        "os.path.join(INSTANCE_ROOT, 'local_config_overrides.py')",
        'Path to local overrides to the instance configuration.'
    ),
]

config_constants_external = [
    ConfigConstant(
        'EXTERNAL_CONFIG_SOURCES',
        "os.path.join(INSTANCE_ROOT, 'external_configs.yaml')",
        "Path to a yaml definition file mapping to external config sources."
    )
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))

    manager.load_elements(config_constants_environment,
                          doc="Environment Variable Override Configuration")

    manager.load_elements(config_constants_basic,
                          doc="EBS API Server Instance Root")

    if os.path.exists(os.path.join(manager.INSTANCE_ROOT, 'redirect')):
        logger.info("Found instance redirect")
        with open(os.path.join(manager.INSTANCE_ROOT, 'redirect'), 'r') as f:
            manager.INSTANCE_ROOT = f.read().strip()

    manager.load_elements(config_constants_redirected,
                          doc="EBS API Server Configuration Paths")

    manager.load_elements(config_constants_external,
                          doc="External Configuration Paths")

    manager.load_config_files()
