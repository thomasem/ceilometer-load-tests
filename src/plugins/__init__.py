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
from graphite import GraphiteDriver
from log import LogDriver
from statsD import StatsDDriver

mapping = {'log': LogDriver,
           'graphite': GraphiteDriver,
           'statsd': StatsDDriver}


def initialize_plugins(test_name, plugin_conf):
    plugin_list = []
    for name, plugin in mapping.iteritems():
        if name in plugin_conf:
            plugin_list.append(plugin(test_name, **plugin_conf[name]))
    return plugin_list


def invoke(method, plugins, *args, **kwargs):
    for plugin in plugins:
        getattr(plugin, method)(*args, **kwargs)
