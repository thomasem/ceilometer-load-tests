Ceilometer Load Tests
=====================

Load tests for Ceilometer storage drivers.

Tracking tests here: https://etherpad.openstack.org/p/ceilometer-data-store-scale-testing

Getting Started (hopefully fast :)
----------------

First, a few packages that could be installed to help with a fresh distribution (specifically using Debian Squeeze):

```
libmysqlclient-dev
libpq-dev
```

Second, you need to install your desired branch of Ceilometer to test. We have a fork set aside for instrumentation here: https://github.com/rackerlabs/instrumented-ceilometer.

Once you pull down the repository, it's important to install the requirements for Ceilometer to work, this will pick up the database driver dependencies for you.

```
cd ./ceilometer
pip install -r requirements.txt
python setup.py install
```

After that, pull down this repository and install the few additional requirements:

```
cd ./ceilometer-load-tests
pip install -r requirements.txt
```

Afterwards, you need to configure the setup script:

```
cp ./etc/test_setup_sample.py ./src/test_setup.py
```

This setup file ought to have some okay defaults to start with. There are three plugins already available (graphite, log, and statsd), you can take a look at their ```__init__(...)``` constructor signature to see what attributes need to be set in the plugins configuration (```plugins={...}```) in test_setup.py. That configuration is basically just exploded into the keyword arguments for initializing the plugins.

After you have this configuration set to your liking, with the ```db_conn``` URI referencing your database, you can run ```python time_inserts.py --help``` to get the current CLI parameters to configure each test.


**Here's an example for reference**:
```
$ python time_inserts.py -h
usage: time_inserts.py [-h] --name NAME [--events EVENTS] [--batch BATCH]
                       [--publish PUBLISH] [--rest REST] [--store STORE]
                       [--pool POOL] [--journaling]
                       [--write_concern WRITE_CONCERN] [--sharding]

Time Inserting Events

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  Name of the test; used for publishing stats.
  --events EVENTS, -e EVENTS
                        Number of events to insert during test. Default: 1000
  --batch BATCH, -b BATCH
                        Number of events to generate before sending to the
                        database. Default: 100
  --publish PUBLISH, -p PUBLISH
                        Number of batches to accumulate beforepublishing
                        stats. Default: 2
  --rest REST, -r REST  Seconds to rest between batches. Default: 0
  --store STORE, -s STORE
                        Filename to store pool dump with.
  --pool POOL, -f POOL  Input filename for a randomizer pool dump file.
  --journaling, -j      Enable journaling, if the datastore supports it.
  --write_concern WRITE_CONCERN, -w WRITE_CONCERN
                        Write concern level, if the datastore supports it.
                        Default: 1
  --sharding            Enforce a sharded datastore, if supported.
```

**Example output from running script**:
```
$ python time_inserts.py -n "thomas test 11" -e 1000
11655 | 2013-12-03 22:17:20.050 | ceilometer.storage.impl_mongodb [-] Connecting to MongoDB on [('localhost', 27017)]
11655 | 2013-12-03 22:17:20.874 | statsd.client.Timer [-] tom_test_17.batch_time: 564.90397453ms
11655 | 2013-12-03 22:17:20.875 | statsd.client.Timer [-] tom_test_17.seconds_per_event: 2.82451987ms
11655 | 2013-12-03 22:17:20.875 | statsd.client.Gauge [-] tom_test_17.events_per_second: 354.042472732
11655 | 2013-12-03 22:17:20.875 | statsd.client.Gauge [-] tom_test_17.total_events: 200
11655 | 2013-12-03 22:17:20.875 | statsd.client.Counter [-] tom_test_17.events: 200
11655 | 2013-12-03 22:17:20.875 | statsd.client.Counter [-] tom_test_17.failed_events: 0
11655 | 2013-12-03 22:17:20.875 | plugins.log [-] Inserted 200 events in 0:00:00.564904	Total inserted: 200
11655 | 2013-12-03 22:17:21.617 | statsd.client.Timer [-] tom_test_17.batch_time: 547.08909988ms
11655 | 2013-12-03 22:17:21.617 | statsd.client.Timer [-] tom_test_17.seconds_per_event: 2.73544550ms
11655 | 2013-12-03 22:17:21.617 | statsd.client.Gauge [-] tom_test_17.events_per_second: 365.571165725
11655 | 2013-12-03 22:17:21.617 | statsd.client.Gauge [-] tom_test_17.total_events: 400
11655 | 2013-12-03 22:17:21.617 | statsd.client.Counter [-] tom_test_17.events: 200
11655 | 2013-12-03 22:17:21.618 | statsd.client.Counter [-] tom_test_17.failed_events: 0
11655 | 2013-12-03 22:17:21.618 | plugins.log [-] Inserted 200 events in 0:00:00.547089	Total inserted: 400
11655 | 2013-12-03 22:17:22.391 | statsd.client.Timer [-] tom_test_17.batch_time: 534.33895111ms
11655 | 2013-12-03 22:17:22.391 | statsd.client.Timer [-] tom_test_17.seconds_per_event: 2.67169476ms
11655 | 2013-12-03 22:17:22.392 | statsd.client.Gauge [-] tom_test_17.events_per_second: 374.294255705
11655 | 2013-12-03 22:17:22.392 | statsd.client.Gauge [-] tom_test_17.total_events: 600
11655 | 2013-12-03 22:17:22.392 | statsd.client.Counter [-] tom_test_17.events: 200
11655 | 2013-12-03 22:17:22.392 | statsd.client.Counter [-] tom_test_17.failed_events: 0
11655 | 2013-12-03 22:17:22.392 | plugins.log [-] Inserted 200 events in 0:00:00.534339	Total inserted: 600
11655 | 2013-12-03 22:17:23.210 | statsd.client.Timer [-] tom_test_17.batch_time: 623.27718735ms
11655 | 2013-12-03 22:17:23.210 | statsd.client.Timer [-] tom_test_17.seconds_per_event: 3.11638594ms
11655 | 2013-12-03 22:17:23.210 | statsd.client.Gauge [-] tom_test_17.events_per_second: 320.884518253
11655 | 2013-12-03 22:17:23.210 | statsd.client.Gauge [-] tom_test_17.total_events: 800
11655 | 2013-12-03 22:17:23.210 | statsd.client.Counter [-] tom_test_17.events: 200
11655 | 2013-12-03 22:17:23.211 | statsd.client.Counter [-] tom_test_17.failed_events: 0
11655 | 2013-12-03 22:17:23.211 | plugins.log [-] Inserted 200 events in 0:00:00.623277	Total inserted: 800
11655 | 2013-12-03 22:17:23.964 | statsd.client.Timer [-] tom_test_17.batch_time: 561.24114990ms
11655 | 2013-12-03 22:17:23.964 | statsd.client.Timer [-] tom_test_17.seconds_per_event: 2.80620575ms
11655 | 2013-12-03 22:17:23.964 | statsd.client.Gauge [-] tom_test_17.events_per_second: 356.353057923
11655 | 2013-12-03 22:17:23.964 | statsd.client.Gauge [-] tom_test_17.total_events: 1000
11655 | 2013-12-03 22:17:23.964 | statsd.client.Counter [-] tom_test_17.events: 200
11655 | 2013-12-03 22:17:23.965 | statsd.client.Counter [-] tom_test_17.failed_events: 0
11655 | 2013-12-03 22:17:23.965 | plugins.log [-] Inserted 200 events in 0:00:00.561241	Total inserted: 1000
11655 | 2013-12-03 22:17:23.965 | plugins.log [-] ===========================================================================
11655 | 2013-12-03 22:17:23.965 | plugins.log [-] Total time to insert 1000 documents: 0:00:02.830850
11655 | 2013-12-03 22:17:23.965 | plugins.log [-] Average time per event: 0:00:00.002831
11655 | 2013-12-03 22:17:23.966 | plugins.log [-] Average events per second: 353.250745129
```

*Note: Please open up a GitHub issue for any problems you run into.*
