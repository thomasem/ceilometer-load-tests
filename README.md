Ceilometer Load Tests
=====================

Load tests for Ceilometer storage drivers.

Tracking tests here: https://etherpad.openstack.org/p/ceilometer-data-store-scale-testing

Getting Started (hopefully fast :)
----------------

First, you need to install your desired branch of Ceilometer to test. We have a fork set aside for instrumentation here: https://github.com/rackerlabs/instrumented-ceilometer.

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
                       [--pool POOL]

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
```

**Example output from running script**:
```
$ python time_inserts.py -n "thomas test 11" -e 1000
17719 | 2013-11-26 19:42:37.416 | ceilometer.storage.impl_mongodb [-] connecting to MongoDB on mongodb://localhost:27017/ceilometer
17719 | 2013-11-26 19:42:38.397 | statsd.client.Timer [-] thomas test 11.batch_time: 750.46086311ms
17719 | 2013-11-26 19:42:38.397 | statsd.client.Gauge [-] thomas test 11.events_per_second: 266.502904855
17719 | 2013-11-26 19:42:38.397 | statsd.client.Counter [-] thomas test 11.events: 200
17719 | 2013-11-26 19:42:38.397 | plugins.log [-] Inserted 200 events in 0:00:00.750461	Total inserted: 200
17719 | 2013-11-26 19:42:39.314 | statsd.client.Timer [-] thomas test 11.batch_time: 745.11122704ms
17719 | 2013-11-26 19:42:39.314 | statsd.client.Gauge [-] thomas test 11.events_per_second: 268.416301813
17719 | 2013-11-26 19:42:39.314 | statsd.client.Counter [-] thomas test 11.events: 200
17719 | 2013-11-26 19:42:39.315 | plugins.log [-] Inserted 200 events in 0:00:00.745111	Total inserted: 400
17719 | 2013-11-26 19:42:40.001 | statsd.client.Timer [-] thomas test 11.batch_time: 510.25605202ms
17719 | 2013-11-26 19:42:40.001 | statsd.client.Gauge [-] thomas test 11.events_per_second: 391.960074181
17719 | 2013-11-26 19:42:40.001 | statsd.client.Counter [-] thomas test 11.events: 200
17719 | 2013-11-26 19:42:40.001 | plugins.log [-] Inserted 200 events in 0:00:00.510256	Total inserted: 600
17719 | 2013-11-26 19:42:40.738 | statsd.client.Timer [-] thomas test 11.batch_time: 540.01021385ms
17719 | 2013-11-26 19:42:40.738 | statsd.client.Gauge [-] thomas test 11.events_per_second: 370.363365117
17719 | 2013-11-26 19:42:40.738 | statsd.client.Counter [-] thomas test 11.events: 200
17719 | 2013-11-26 19:42:40.739 | plugins.log [-] Inserted 200 events in 0:00:00.540010	Total inserted: 800
17719 | 2013-11-26 19:42:41.494 | statsd.client.Timer [-] thomas test 11.batch_time: 575.04892349ms
17719 | 2013-11-26 19:42:41.494 | statsd.client.Gauge [-] thomas test 11.events_per_second: 347.796494923
17719 | 2013-11-26 19:42:41.494 | statsd.client.Counter [-] thomas test 11.events: 200
17719 | 2013-11-26 19:42:41.494 | plugins.log [-] Inserted 200 events in 0:00:00.575049	Total inserted: 1000
17719 | 2013-11-26 19:42:41.495 | plugins.log [-] ===========================================================================
17719 | 2013-11-26 19:42:41.495 | plugins.log [-] Total time to insert 1000 documents: 0:00:03.120887
17719 | 2013-11-26 19:42:41.495 | plugins.log [-] Average time per event: 0:00:00.003121
17719 | 2013-11-26 19:42:41.495 | plugins.log [-] Average events per second: 320.421697562
```

*Note: Please open up a GitHub issue for any problems you run into.*
