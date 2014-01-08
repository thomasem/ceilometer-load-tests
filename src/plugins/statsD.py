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
"""StatsD plugins for Ceilometer load testing.
"""

import statsd

import base


class StatsDDriver(base.PluginBase):
    """Sends metrics to StatsD.
    """

    def __init__(self, test_name, host='localhost', port=8125, sample_rate=1):
        """Configure the plugin with what StatsD host to talk to and how.
        """
        super(StatsDDriver, self).__init__()
        conn = statsd.Connection(host=host, port=port, sample_rate=sample_rate)
        self.client = statsd.Client(test_name, conn)
        self.gauge = self.client.get_client(class_=statsd.Gauge)

    def publish(self, stats, **kwargs):
        for k, v in stats.iteritems():
            self.gauge.send(k, v)
