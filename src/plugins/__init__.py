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
"""Plugins module for Ceilometer load testing.
"""


def load_plugins(plugin_conf):
    """Load plugins from a passed in configuration

    :Example:
    plugins = {
        graphite.GraphitePlugin: {
            'host': <host_address>,
            'port': <port>,
            'path': 'ceilometer.load-tests.mongo_2_4_8',
            'resolution': 300
        },
        <relative_plugin_path>: {
            'param_1': ...,
            'param_2': ...,
            'param_3': ...
        },
        ...
    }
    """
    instantiated_plugins = []
    plugins = __import__('plugins')
    for path, conf in plugin_conf.iteritems():
        tokenized = path.split('.')
        classname = tokenized[-1]
        module = plugins
        for mod in tokenized[:-1]:
            module = getattr(plugins, mod)
        plugin = getattr(module, classname)
        instantiated_plugins.append(plugin(**conf))
    return instantiated_plugins
