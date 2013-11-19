#!/usr/bin/env python

from datetime import timedelta
import time

from ceilometer import storage
from ceilometer.openstack.common import log
from oslo.config import cfg

from rando import RandomEventGenerator
import test_settings

cfg.CONF.set_override("connection", test_settings.db_conn, group='database')
cfg.CONF.set_override("verbose", True)
cfg.CONF.set_override("logging_default_format_string",
                      '%(process)d | %(asctime)s.%(msecs)03d |'
                      ' %(pathname)s [-] %(instance)s%(message)s')

LOG = log.getLogger(__name__)
log.setup("Ceilometer Load Test")


if __name__ == "__main__":
    conn = storage.get_connection(cfg.CONF)
    rand = RandomEventGenerator(**test_settings.__dict__)
    total_seconds = 0
    delta_history = []

    revs = test_settings.num_events / test_settings.batch_size
    log_frequency = test_settings.log_frequency
    for x in range(1, revs + 1):
        start = time.time()
        conn.record_events(
            rand.generate_random_events(test_settings.batch_size))
        end = time.time()
        total_seconds += end - start

        if x % log_frequency == 0:
            delta_history.append(total_seconds)
            log_msg = ("Inserted %d events in %d sized batches in "
                       "%s\tTotal inserted: %d" %
                       (log_frequency * test_settings.batch_size,
                        test_settings.batch_size,
                        str(timedelta(seconds=total_seconds)),
                        x * test_settings.batch_size))
            LOG.info(log_msg)
            total_seconds = 0
        time.sleep(test_settings.rest_time)

    total = sum(delta_history)

    LOG.info("".join("=" for x in range(75)))
    log_msg = 'Total time to insert %d documents: %s' % \
        (test_settings.num_events, str(timedelta(seconds=total)))
    LOG.info(log_msg)

    avg_per_log = total / (test_settings.num_events / test_settings.batch_size)
    log_msg = 'Average per %d events: %s' % (
              (test_settings.batch_size,
               str(timedelta(seconds=avg_per_log))))
    LOG.info(log_msg)

    avg_per_event = total / test_settings.num_events
    log_msg = 'Average per event: %s' % (
              (str(timedelta(seconds=avg_per_event))))
    LOG.info(log_msg)
