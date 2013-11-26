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

import socket
import time

from base import PluginBase


class GraphiteDriver(PluginBase):
    """Sends metrics to graphite.
    """

    def __init__(self, graphite_host, graphite_port, graphite_path,
                 graphite_resolution):
        """Configure the plugin with what graphite host to talk to and how.
        """
        super(GraphiteDriver, self).__init__()
        self.host = graphite_host
        self.port = graphite_port
        self.path = graphite_path
        self.res = graphite_resolution
        self.mask = "%s %s %d\n"

    def _send_to_graphite(self, metric, value):
        """Send a metric to graphite using the configured path and timestamp
        nearest to the resolution.
        """
        timestamp = round(time.time() / self.res) * self.res
        full_path = "%s%s" % (self.path, metric)
        sock = socket.socket()
        sock.connect((self.host, self.port))
        sock.sendall(self.mask % (full_path, value, timestamp))
        sock.close()

    def publish(self, stats, **kwargs):
        total, batch_size, seconds = (stats['total_stored'],
                                      stats['batch_size'], stats['seconds'])
        self._send_to_graphite('total', total)
        self._send_to_graphite('seconds', seconds)
        self._send_to_graphite('events_per_second',
                               float(batch_size) / seconds)

    def after_test(self, totals, **kwargs):
        pass
