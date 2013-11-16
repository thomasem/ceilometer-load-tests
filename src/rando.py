#!/usr/bin/env python

#system libraries
import datetime
import random
import uuid

#third-party libraries
from ceilometer.storage.models import Event
from ceilometer.storage.models import Trait

#application libraries
import test_settings
from pools import events_pool
from pools import keys_types_pool
from pools import strings_pool


class RandoCalrissian(object):

    def get_next_generated(self):
        """Gets the next generated event timestamp.

        :Note: Given some potential, it may also have a negative delta to
        simulate messages out of order.
        """
        negative_boundary = -test_settings.rand_generated_potential / \
            test_settings.message_order_integerity
        delta = random.randint(negative_boundary,
                               test_settings.rand_generated_potential)
        self.last_generated = self.last_generated + \
            datetime.timedelta(seconds=delta)
        return self.last_generated

    def generate_random_integer(self):
        """Generates a random integer from pre-set constraints
        """
        return random.randint(test_settings.rand_int_start,
                              test_settings.rand_int_start +
                              test_settings.rand_int_range)

    def generate_random_float(self):
        """Generates a random float (usually) based on the random integers.
        """
        return float(self.generate_random_integer()) / \
            self.generate_random_integer()

    def generate_random_text(self):
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

    def generate_random_events(self, quantity):
        """Generates N random events.
        """
        event_models = []
        pool_len = len(events_pool)
        for x in range(quantity):
            key_types = random.sample(keys_types_pool,
                                      test_settings.num_traits_per_doc)
            trait_models = self._make_traits(key_types)
            event_models.append(Event(str(uuid.uuid4()),
                                events_pool[random.randrange(0, pool_len)],
                                self.get_next_generated(), trait_models))
        return event_models

    def __init__(self):
        self.last_generated = datetime.datetime.utcnow()
        self._rand_type_map = {
            't_int': self.generate_random_integer,
            't_float': self.generate_random_float,
            't_datetime': self.generate_random_datetime,
            't_text': self.generate_random_text
        }
