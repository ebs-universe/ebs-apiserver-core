#!/usr/bin/env python
# encoding: utf-8

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

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from tendril.utils.config import ConfigManager
_manager = ConfigManager(prefix='ebs.apiserver.config',
                         legacy=None,
                         excluded=[])

import sys
sys.modules[__name__] = _manager
