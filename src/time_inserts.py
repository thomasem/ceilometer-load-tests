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
"""Ceilometer load testing application.
"""

import time

from ceilometer import storage
from oslo.config import cfg

from rando import RandomEventGenerator
import test_setup

cfg.CONF.set_override("connection", test_setup.db_conn, group='database')


def invoke_plugins(method, *args, **kwargs):
    for name, plugin in test_setup.plugins:
        getattr(plugin, method)(*args, **kwargs)

if __name__ == "__main__":
    conn = storage.get_connection(cfg.CONF)
    rand = RandomEventGenerator(**test_setup.__dict__)
    total_seconds = 0
    delta_history = []

    revs = test_setup.num_events / test_setup.batch_size
    publish_frequency = test_setup.publish_frequency
    for x in range(1, revs + 1):
        start = time.time()
        conn.record_events(
            rand.generate_random_events(test_setup.batch_size))
        end = time.time()
        total_seconds += end - start

        if x % publish_frequency == 0:
            delta_history.append(total_seconds)
            stats = {'stored': publish_frequency * test_setup.batch_size,
                     'batch_size': test_setup.batch_size,
                     'time': total_seconds,
                     'total_inserted': x * test_setup.batch_size}
            invoke_plugins('publish', stats)
            total_seconds = 0
        time.sleep(test_setup.rest_time)

    totals = {'total_seconds': sum(delta_history),
              'total_events': test_setup.num_events}
    invoke_plugins('after_test', totals)
