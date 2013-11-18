#!/usr/bin/env python


# Database settings
db_conn = "mysql://root:password@localhost/ceilometer?charset=utf8"

# Tester settings
num_events = 500000
log_frequency = 1000
batch_size = 10

# Randomizer settings
extra_traits_per_event = 50
rand_int_start = 12897
rand_int_range = 40
timestamp_start = 1262304000
timestamp_end = 1356955199
rand_generated_potential = 20
message_order_integrity = 4
