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

from datetime import timedelta

from ceilometer.openstack.common import log
from oslo.config import cfg

from base import PluginBase

cfg.CONF.set_override("verbose", True)
cfg.CONF.set_override("logging_default_format_string",
                      '%(process)d | %(asctime)s.%(msecs)03d |'
                      ' %(name)s [-] %(instance)s%(message)s')

LOG = log.getLogger(__name__)


class LogDriver(PluginBase):
    """Sends metrics to graphite.
    """

    def __init__(self, log_name):
        """Configure the plugin with what graphite host to talk to and how.
        """
        super(LogDriver, self).__init__()
        log.setup(log_name)

    def publish(self, stats, **kwargs):
        log_msg = ("Inserted %d events in %d sized batches in "
                   "%s\tTotal inserted: %d" %
                   (stats['stored'], stats['batch_size'],
                    str(timedelta(seconds=stats['seconds'])),
                    stats['total_stored']))
        LOG.info(log_msg)

    def after_test(self, totals, **kwargs):
        total_events = totals['total_events']
        total_time = totals['total_seconds']
        LOG.info("".join("=" for x in range(75)))
        log_msg = 'Total time to insert %d documents: %s' % \
            (total_events, str(timedelta(seconds=total_time)))
        LOG.info(log_msg)

        avg_per_event = total_time / total_events
        log_msg = 'Average time per event: %s' % (
                  (str(timedelta(seconds=avg_per_event))))
        LOG.info(log_msg)

        avg_events_per_sec = total_events / total_time
        log_msg = 'Average events per second: %s' % (avg_events_per_sec)
        LOG.info(log_msg)
