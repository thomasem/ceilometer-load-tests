#!/usr/bin/env python

#stdlib
import datetime
import random
import time
import uuid

#third-party
from ceilometer.storage.models import Event
from ceilometer.storage.models import Trait

#application
from pools import events_pool
from pools import keys_types_pool
from pools import strings_pool


class RandomEventGenerator(object):

    def _get_next_generated(self):
        """Gets the next generated event timestamp.

        :Note: Given some potential, it may also have a negative delta to
        simulate messages out of order.
        """
        negative_boundary = -float(self.rand_generated_potential) / \
            self.message_order_integrity
        delta = random.randint(negative_boundary,
                               self.rand_generated_potential)
        self.last_generated = self.last_generated + \
            datetime.timedelta(seconds=delta)
        return self.last_generated

    def _generate_random_timestamp(self):
        """Returns a random datetime from from_time to to_time (UNIX ts)
        """
        return datetime.datetime.utcfromtimestamp(
            random.randint(self.timestamp_start, self.timestamp_end))

    def _generate_random_integer(self):
        """Generates a random integer from pre-set constraints
        """
        return random.randint(self.rand_int_start,
                              self.rand_int_start +
                              self.rand_int_range)

    def _generate_random_float(self):
        """Generates a random float.
        """
        return random.random()

    def _generate_random_text(self):
        """Chooses a random string from a pre-made string pool.
        """
        return random.choice(strings_pool)

    def _make_traits(self, key_types):
        """Given a list of (key, type) tuples, make a key-value traits list.
        """
        traits = []
        for key_type in key_types:
            _key, _type = key_type
            traits.append(Trait(_key, _type, self._rand_type_map[_type]()))
        return traits

    def _create_random_event(self):
        key_types = random.sample(keys_types_pool,
                                  self.traits_per_event)
        trait_models = self._make_traits(key_types)
        pool_len = len(events_pool)
        return Event(str(uuid.uuid4()),
                     events_pool[random.randrange(0, pool_len)],
                     self._get_next_generated(), trait_models)

    def generate_random_events(self, quantity):
        """Generates N random events.
        """
        event_models = []
        for x in range(quantity):
            event_models.append(self._create_random_event())
        return event_models

    def generate_random_event(self):
        return self._create_random_event()

    def __init__(self, rand_int_start=0, rand_int_range=100,
                 timestamp_start=None, timestamp_end=None,
                 traits_per_event=20, message_order_integrity=3,
                 rand_generated_potential=10, **kwargs):
        self.last_generated = datetime.datetime.utcnow()
        self.rand_int_start = rand_int_start
        self.rand_int_range = rand_int_range
        self.traits_per_event = traits_per_event
        self.rand_generated_potential = rand_generated_potential
        self.message_order_integrity = message_order_integrity
        self.timestamp_start = timestamp_start or int(time.time())
        self.timestamp_end = timestamp_end or (self.ts_start + 86400)
        self._rand_type_map = {
            Trait.INT_TYPE: self._generate_random_integer,
            Trait.FLOAT_TYPE: self._generate_random_float,
            Trait.DATETIME_TYPE: self._generate_random_timestamp,
            Trait.TEXT_TYPE: self._generate_random_text
        }
