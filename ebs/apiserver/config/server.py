# Copyright (C) 2022 Chintalagiri Shashank
#
# This file is part of EBS API Server.
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
Server Configuration Options
============================
"""


from tendril.utils.config import ConfigOption

import logging
logger = logging.getLogger(__name__)

depends = ['ebs.apiserver.config.core']


config_elements_server = [
    ConfigOption(
        'BIND_IP', "'0.0.0.0'",
        "IP Address the server should bind to. See uvicorn.Server and uvicorn.Config."
    ),
    ConfigOption(
        'PORT', "8039",
        "Port the server should listen on.",
        parser=int
    ),
    ConfigOption(
        'ENABLE_SSL', "True",
        "Whether to use TLS/SSL connections.",
        parser=bool
    ),
    ConfigOption(
        'SSL_KEYFILE', "''",
        "Path to the SSL Key to use."
    ),
    ConfigOption(
        'SSL_CERTFILE', "''",
        "Path to the SSL Certificate to use."
    )
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_server,
                          doc="API Server Configuration")
