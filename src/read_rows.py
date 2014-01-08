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

import plugins
import pools
import rando
import test_base
import test_setup

cfg.CONF.set_override("connection", test_setup.db_conn, group='database')


class ReadTest(test_base.BaseTest):

    def __init__(self, query_generator, conn, settings):
        self.conn = conn
        self.settings = settings
        self.query_generator = query_generator

    def run_test(self, publish):
        while True:
            total_seconds = 0
            event_filter = self.query_generator.create_random_filter()
            start = time.time()
            conn.get_events(event_filter)
            end = time.time()
            total_seconds += end - start
            stats = {
                'query_time': total_seconds,
            }
            plugins.invoke('publish_read', plugin_list, stats)
            time.sleep(self.rest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time Inserting Events")

    parser.add_argument('--name', '-n', type=str, required=True,
                        help="Name of the test; used for publishing stats.")
    parser.add_argument('--rest', '-r', type=int, default=0,
                        help="Seconds to rest between queries. Default: 0")
    parser.add_argument('--pool', '-f', type=str, default=None, required=True,
                        help=("Input filename for a randomizer pool dump file."
                              "This is needed to define the query parameters.")
                        )
    parser.add_argument('--number_of_traits', '-t', type=str, default=1,
                        help="Number of random trait filters to generate.")

    args = parser.parse_args()
    pool = pools.Pool.from_snapshot(args.pool)
    plugin_list = plugins.initialize_plugins(args.name, test_setup.plugins)
    conn = storage.get_connection(cfg.CONF)
    query_generator = rando.RandomQueryGenerator(pool, args)

    test = ReadTest(query_generator, conn, args)
    test.run_test(publish=lambda x: plugins.invoke('publish', plugin_list, x))
