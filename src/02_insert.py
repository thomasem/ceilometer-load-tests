#!/usr/bin/env python

import random
import logging
import datetime
import pymongo
import uuid

import cfg

def random_utc_datetime(from_time, to_time):
    '''Returns a random datetime from from_time to to_time (UNIX ts)'''

    if from_time <= 0 or to_time <= 0:
        return None
    elif from_time > to_time:
        return datetime.datetime.utcfromtimestamp(from_time)
    else:
        return datetime.datetime.utcfromtimestamp(
                                    random.randint(from_time, to_time))


def make_traits(keys_types):
    '''Given a list of (key, type) tuples, make a key-value traits list.'''

    traits = []

    for thing in keys_types:
        _key, _type = thing
        if _type == 'int':
            _value = random.randint(cfg.rand_int_start,
                                    cfg.rand_int_start + cfg.rand_int_range)
        elif _type == 'str':
            _value = random.choice(cfg.strings_pool)
        elif _type == 'datetime':
            _value = random_utc_datetime(cfg.timestamp_start,
                                               cfg.timestamp_end)
        # traits.append({"key": _key, "value": _value})
        traits.append({_key: _value})

    return traits


#
# Set up a logger
#

log = logging.getLogger('insert_02')
log.setLevel(logging.INFO)
fh = logging.FileHandler('insert_02.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)


#
# MongoDB connection + DB/collection handles
#

mongo_uri = 'mongodb://%s:%s@%s/%s' % (
    (cfg.db_user, cfg.db_passwd, cfg.db_server, cfg.db_name))

mongo_client = pymongo.MongoReplicaSetClient(
    mongo_uri, replicaSet=cfg.mongo_repl_set)

mongo_client.write_concern = {'w': 1, 'j': False}
db = mongo_client[cfg.db_name]
collection = db[cfg.collection_name]


#
# Prepare and insert document sets
#

events = cfg.events_pool.values()
events_len = len(events)
num_docs_inserted = 0
t1 = datetime.datetime.utcnow()
delta_sums = datetime.timedelta(seconds=0)
while num_docs_inserted < cfg.num_docs:
    keys_types = random.sample(cfg.keys_types_pool, cfg.num_traits_per_doc)
    doc = {
        '_id': str(uuid.uuid4()),
        'event_name': events[random.randrange(0, events_len)],
        'generated': random_utc_datetime(cfg.timestamp_start,
                                         cfg.timestamp_end),
        'traits': make_traits(keys_types),
    }
    collection.insert(doc)
    num_docs_inserted += 1
    if num_docs_inserted % cfg.log_frequency_docs == 0:
        t2 = datetime.datetime.utcnow()
        delta = t2 - t1
        log_msg = 'inserted %8d documents ; inserted %d docs in %s' % (
                    (num_docs_inserted, cfg.log_frequency_docs, str(delta)))
        log.info(log_msg)
        delta_sums += delta
        t1 = t2
    del keys_types
    del doc
log_msg = 'Total time to insert %8d documents: %s' % (cfg.num_docs, str(delta_sums))
log.info(log_msg)
avg_delta_per_log_unit = delta_sums / (cfg.num_docs / cfg.log_frequency_docs)
log_msg = 'Average per %d documents: %s' % (
            (cfg.log_frequency_docs, str(avg_delta_per_log_unit)))
log.info(log_msg)
mongo_client.disconnect()
