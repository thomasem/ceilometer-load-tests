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
"""Settings for Ceilometer load testing.
"""

from plugins import LogDriver

# Database settings
# db_conn = "mysql://user:password@localhost/ceilometer?charset=utf8"
db_conn = "mongodb://localhost:27017/ceilometer"

# Tester settings
num_events = 500000             # Number of events to try and store during test
batch_size = 1000               # Events per storage call
publish_frequency = 1           # Number of batches, not events
rest_time = 0                   # Time to rest between batches

# Randomizer settings
extra_traits_per_event = 50     # Additional random traits to append
extra_traits_pool_size = 50     # Extra traits for messages
random_str_pool_size = 100      # Extra strings for additional random traits
rand_int_start = 12897          # Starting point for randint(...)
rand_int_range = 40             # Range from starting point for randint(...)
timestamp_start = 1262304000    # Start of timestamp range in unix time
timestamp_end = 1356955199      # End of timestamp range in unix time
rand_generated_potential = 10   # Potential time for next 'generated' trait
message_order_integrity = 5     # Rank of integrity for message ordering (1-5)

# Plugin settings
# We'll simply do this until we start using Stevedore for extension management.
plugins = {
    'log': LogDriver("Ceilometer Load Test"),
}
