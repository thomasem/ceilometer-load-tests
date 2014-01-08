# -*- encoding: utf-8 -*-
#
# Copyright © 2013 Rackspace Hosting
#
# Author: Thomas Maddox <thomas.maddox@rackspace.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Graphite plugins for Ceilometer load testing.
"""

from ceilometer.openstack.common import log
from oslo.config import cfg

import base

cfg.CONF.set_override("verbose", True)
cfg.CONF.set_override("logging_default_format_string",
                      '%(process)d | %(asctime)s.%(msecs)03d |'
                      ' %(name)s [-] %(instance)s%(message)s')

LOG = log.getLogger(__name__)


class LogDriver(base.PluginBase):
    """Sends metrics to graphite.
    """

    def __init__(self, test_name, *args, **kwargs):
        """Configure the plugin with what graphite host to talk to and how.
        """
        super(LogDriver, self).__init__()
        log.setup(test_name)

    def publish(self, stats, **kwargs):
        for k, v in stats.iteritems():
            LOG.info('%s:\t%s' % (k, v))
