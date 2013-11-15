import datetime
import os

from ceilometer.openstack.common import log
from ceilometer import storage
from ceilometer.storage import models

from oslo.config import cfg

LOG = log.getLogger(__name__)
log.setup('Ceilometer Load Test')

# LOAD_TEST_CONN = "mysql://username:password@127.0.0.1/ceilometer?charset=utf8"
connection_string = os.environ['LOAD_TEST_CONN']

cfg.CONF.set_override("connection", connection_string, group='database')
conn = storage.get_connection(cfg.CONF)

event_models = []
base = 0
now = datetime.datetime(2013, 12, 31, 5, 0)
for event_name in ['Foo', 'Bar', 'Zoo']:
    trait_models = \
        [models.Trait(name, dtype, value)
            for name, dtype, value in [
                ('trait_A', models.Trait.TEXT_TYPE,
                    "my_%s_text" % event_name),
                ('trait_B', models.Trait.INT_TYPE,
                    base + 1),
                ('trait_C', models.Trait.FLOAT_TYPE,
                    float(base) + 0.123456),
                ('trait_D', models.Trait.DATETIME_TYPE, now)]]
    event_models.append(
        models.Event("id_%s" % event_name,
                     event_name, now, trait_models))
    base += 100
    now = now + datetime.timedelta(hours=1)

conn.record_events(event_models)
