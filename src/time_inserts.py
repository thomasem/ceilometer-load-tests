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
from pymongo import errors

import plugins
import pools
import rando
import test_base
import test_setup

cfg.CONF.set_override("connection", test_setup.db_conn, group='database')


class InsertTest(test_base.BaseTest):

    def __init__(self, event_generator, conn, settings):
        self.event_generator = event_generator
        self.conn = conn
        self.settings = settings
        if test_setup.db_conn.startswith('mongodb'):
            conn.write_concern = {'w': settings.write_concern,
                                  'j': settings.journaling}
            if settings.sharding:
                try:
                    conn.conn.admin.command('enablesharding', 'ceilometer')
                    conn.conn.admin.command('shardcollection',
                                            'ceilometer.event',
                                            key={'_id': "hashed"})
                except errors.OperationFailure:
                    pass

    def run_test(self, publish=lambda x: x):
        total_seconds = 0
        total_failed = 0
        delta_history = []
        revs = self.settings.events / self.settings.batch
        publish_frequency = self.settings.publish
        for x in range(1, revs + 1):
            events = self.event_generator.generate_random_events(
                self.settings.batch)
            start = time.time()
            failed = conn.record_events(events)
            end = time.time()
            total_seconds += end - start
            total_failed += len(failed)

            if x % publish_frequency == 0:
                delta_history.append(total_seconds)
                stats = {'seconds': total_seconds,
                         'events_per_second': float(self.settings.batch) /
                         total_seconds,
                         'total': x * self.settings.batch,
                         'failed': total_failed}
                publish(stats)
                total_seconds = 0
                total_failed = 0
                time.sleep(self.settings.rest)

        totals = {'total_seconds': sum(delta_history),
                  'total_events': self.settings.events}
        publish(totals)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time Inserting Events")

    parser.add_argument('--name', '-n', type=str, required=True,
                        help="Name of the test; used for publishing stats.")
    parser.add_argument('--events', '-e', type=int, default=1000,
                        help=("Number of events to insert during test. "
                              "Default: 1000"))
    parser.add_argument('--batch', '-b', type=int, default=100,
                        help=("Number of events to generate before sending to "
                              "the database. Default: 100"))
    parser.add_argument('--publish', '-p', type=int, default=2,
                        help=("Number of batches to accumulate before"
                              "publishing stats. Default: 2"))
    parser.add_argument('--rest', '-r', type=int, default=0,
                        help="Seconds to rest between batches. Default: 0")
    parser.add_argument('--store', '-s', type=str, default=None,
                        help="Filename to store pool dump with.")
    parser.add_argument('--pool', '-f', type=str, default=None,
                        help="Input filename for a randomizer pool dump file.")
    parser.add_argument('--journaling', '-j', action='store_true',
                        help=("Enable journaling, if the datastore supports"
                              " it."))
    parser.add_argument('--write_concern', '-w', type=int, default=1,
                        help=("Write concern level, if the datastore supports"
                              " it. Default: 1"))
    parser.add_argument('--sharding', action='store_true',
                        help="Enforce a sharded datastore, if supported.")

    args = parser.parse_args()
    pool = pools.Pool.from_snapshot(args.pool) if args.pool else \
        pools.Pool(args.events, test_setup, store=args.store)
    rand = rando.RandomEventGenerator(pool, test_setup)
    conn = storage.get_connection(cfg.CONF)
    plugin_list = plugins.initialize_plugins(args.name, test_setup.plugins)

    test = InsertTest(rand, conn, args)
    test.run_test(publish=lambda x: plugins.invoke('publish', plugin_list, x))
