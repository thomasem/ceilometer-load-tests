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

import base


class GraphiteDriver(base.PluginBase):
    """Sends metrics to graphite.
    """

    def __init__(self, test_name, host="localhost", port=2003,
                 path="ceilometer-load-test", resolution=60):
        """Configure the plugin with what graphite host to talk to and how.
        """
        super(GraphiteDriver, self).__init__()
        self.host = host
        self.port = port
        self.path = path
        self.res = resolution
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
        for k, v in stats:
            self._send_to_graphite(k, v)
