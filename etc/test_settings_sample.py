#!/usr/bin/env python


# Database settings
# db_conn = "mysql://root:password@localhost/ceilometer?charset=utf8"
db_conn = "mongodb://localhost:27017/ceilometer"

# Tester settings
num_events = 500000             # Number of events to try and store during test
batch_size = 1000               # Events per storage call
log_frequency = 1               # Number of batches, not events
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
