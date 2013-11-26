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
"""Pool generation for OpenStack notification attributes.
"""

import itertools
import random
import string
import uuid

from ceilometer.storage import models


class Pool(object):
    """Pool object used to control instantiation of randomizer pools.
    """

    events_pool = [
        'compute.instance.create.start',
        'compute.instance.create.end',
        'compute.instance.rebuild.start',
        'compute.instance.rebuild.end',
        'compute.instance.resize.prep.start',
        'compute.instance.resize.prep.end',
        'compute.instance.resize.revert.start',
        'compute.instance.resize.revert.end',
        'compute.instance.finish_resize.end',
        'compute.instance.rescue.start',
        'compute.instance.rescue.end',
        'compute.instance.delete.end',
        'compute.instance.exists',
        'compute.instance.update',
        'image.exists',
        'image.create',
        'image.upload',
        'image.activate',
        'image.delete',
        'image.update'
    ]

    def __init__(self, scale, settings):

        t_text = models.Trait.TEXT_TYPE
        t_int = models.Trait.INT_TYPE
        t_float = models.Trait.FLOAT_TYPE
        t_datetime = models.Trait.DATETIME_TYPE

        high_card = 0.088
        med_high_card = 0.011
        med_card = 0.0011
        low_card = 0.000088

        self.scale = scale
        # (TMaddox) thought: we can flex cardinality of trait strings with the
        # pool size configurations.
        self.strings_pool = self._randstrings(settings.random_str_pool_size,
                                              50)
        self.extra_traits_pool = [(key, dtype, None) for (key, dtype) in
                                  itertools.product(self._randstrings(
                                      settings.extra_traits_pool_size, 30),
                                      [t_text, t_datetime, t_int, t_float])]

        # Cardinality ratios for things that will scale with event quantity.
        # Examples:
        #
        # Med_card is like 26K tenants for 24M notifications
        #
        # Med_high_card is like 264K instances referenced in 24M notifications
        #
        # High_card is like 2.1M requests referenced in 24M notifications

        # Mock expected traits to better estimate cardinality.
        priorities = ['error', 'info']
        services = ['api', 'scheduler', 'compute', 'conductor']
        hosts = ["%s-%d" % (s, n) for s, n in
                 itertools.product(services, range(4))]
        tasks = ['task_%d' % t for t in range(20)]
        states = ['state_%s' % n for n in range(20)]
        flavors = ["%s" % str(uuid.uuid4()) for n in range(10)]
        instance_type_ids = range(len(flavors))
        image_types = ['base', 'snapshot']
        os_types = ['linux', 'windows', 'centos']
        distros = ["distro_%s" % n for n in range(3)]
        rax_options = ["%s-%s-%s" % (t, o, d) for t, o, d in
                       itertools.product(image_types, os_types, distros)]

        # Some of these could have too low cardinality to show up with lower
        # scales, so set at least one.
        images = [uuid.uuid4()] + \
            ["%s" % str(uuid.uuid4()) for (o, n) in
             itertools.product(rax_options, range(int(self.scale * low_card)))]

        instances = [uuid.uuid4()] + \
            ["%s" % str(uuid.uuid4()) for n in
             range(int(self.scale * med_high_card))]

        tenants = [uuid.uuid4()] + \
            ["%s" % str(uuid.uuid4()) for n in
             range(int(self.scale * med_card))]

        users = [uuid.uuid4()] + \
            ["%s" % str(uuid.uuid4()) for n in
             range(int(self.scale * med_high_card))]

        request_ids = [uuid.uuid4()] + \
            ["req-%s" % uuid.uuid4() for x in
             range(int(self.scale * high_card))]

        self.compute_keys = [
            ('hostname', t_text, hosts),
            ('request_id', t_text, request_ids),
            ('tenant', t_text, tenants),
            ('user', t_text, users),
            ('uuid', t_text, instances),
            ('owner', t_text, users),
            ('launched_at', t_datetime, None),
            ('deleted_at', t_datetime, None),
            ('instance_flavor_id', t_text, flavors),
            ('instance_type_id', t_int, instance_type_ids),
            ('state', t_text, states),
            ('old_state', t_text, states),
            ('task', t_text, tasks),
            ('old_task', t_text, tasks),
            ('progress', t_int, range(15)),
            ('image_type', t_text, image_types),
            ('os_type', t_text, os_types),
            ('os_distro', t_text, distros),
            ('rax_options', t_text, rax_options),
            ('audit_period_beginning', t_datetime, None),
            ('audit_period_ending', t_datetime, None)
        ]

        self.glance_keys = [
            ('name', t_text, images),
            ('uuid', t_text, images),
            ('owner', t_text, users),
            ('size', t_int, instance_type_ids),
            ('created_at', t_datetime, None),
            ('deleted_at', t_datetime, None),
            ('status', t_text, states),
            ('image_type', t_text, image_types),
            ('os_type', t_text, os_types),
            ('os_distro', t_text, distros),
            ('rax_options', t_text, rax_options),
        ]

        self.required_keys = [
            ('publisher', t_text, hosts),
            ('priority', t_text, priorities)
        ]

    @staticmethod
    def _randstrings(quantity, size):
        return [''.join(random.choice(string.ascii_letters)
                        for n in range(size))
                for n in range(quantity)]
