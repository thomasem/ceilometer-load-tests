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
        self.counter = self.client.get_client(class_=statsd.Counter)
        self.gauge = self.client.get_client(class_=statsd.Gauge)
        self.timer = self.client.get_client(class_=statsd.Timer)

    def publish(self, stats, **kwargs):
        total, stored, seconds, failed = (stats['total_stored'],
                                          stats['stored'], stats['seconds'],
                                          stats['failed'])
        self.timer.send("batch_time", seconds)
        self.timer.send("seconds_per_event", seconds / stored)
        self.gauge.send("events_per_second", stored / seconds)
        self.gauge.send("total_events", total)
        self.counter.increment("events", stored)
        self.counter.increment("failed_events", failed)

    def after_test(self, totals, **kwargs):
        pass
