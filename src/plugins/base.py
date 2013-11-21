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
"""Plugin base classes for ceilometer load tests.
"""

import abc


class PluginBase:
    """Base class for load tester plugins.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """Constructor.
        """

    @abc.abstractmethod
    def after_batch(self):
        """Called after a batch of events are stored.
        """

    @abc.abstractmethod
    def after_log(self):
        """Called after each log interval.
        """

    @abc.abstractmethod
    def after_test(self):
        """Called at the completion of the test.
        """
