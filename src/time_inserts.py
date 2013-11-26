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

import argparse
import time

from ceilometer import storage
from oslo.config import cfg
from pymongo.errors import OperationFailure

import plugins
from rando import RandomEventGenerator
import test_setup

cfg.CONF.set_override("connection", test_setup.db_conn, group='database')


def run_test(event_generator, plugins, conn, settings):
    total_seconds = 0
    delta_history = []
    revs = settings.events / settings.batch
    publish_frequency = settings.publish
    for x in range(1, revs + 1):
        events = event_generator.generate_random_events(settings.batch)
        start = time.time()
        conn.record_events(events)
        end = time.time()
        total_seconds += end - start

        if x % publish_frequency == 0:
            delta_history.append(total_seconds)
            stats = {'stored': publish_frequency * settings.batch,
                     'frequency': settings.publish,
                     'seconds': total_seconds,
                     'total_stored': x * settings.batch}
            plugins.invoke('publish', plugins, stats)
            total_seconds = 0
        time.sleep(test_setup.rest_time)

    totals = {'total_seconds': sum(delta_history),
              'total_events': settings.events}
    plugins.invoke('after_test', plugins, totals)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time Inserting Events")

    parser.add_argument('--name', '-n', type=str, required=True,
                        help="Name of the test; used for publishing stats.")
    parser.add_argument('--events', '-e', type=int, required=True,
                        help="Number of events to insert during test")
    parser.add_argument('--batch', '-b', type=int, default=1,
                        help=("Number of events to generate before sending to"
                              "the driver."))
    parser.add_argument('--publish', '-p', type=int, required=True,
                        help=("Number of batches to accumulate before"
                              "publishing stats."))
    parser.add_argument('--rest', '-r', type=int, default=0,
                        help="Seconds to rest between batches.")

    args = parser.parse_args()

    rand = RandomEventGenerator(**test_setup.__dict__)
    plugin_list = plugins.initialize_plugins(args.name, test_setup.plugins)
    conn = storage.get_connection(cfg.CONF)

    # Before test do this.
    if test_setup.db_conn.startswith('mongodb'):
        if test_setup.ensure_sharding:
            try:
                conn.admin.command('enablesharding', 'ceilometer')
                conn.admin.command('shardcollection', 'ceilometer.event',
                                   key={'_id': 1})
            except OperationFailure:
                pass

    run_test(rand, plugin_list, conn, args)
