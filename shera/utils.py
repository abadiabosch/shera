# -*- encoding: UTF-8 -*-

''' utils from amoniak by gisce 

Author: https://www.gisce.net
See https://github.com/gisce/amoniak 

'''
import os
import logging
import redis
from rq import Queue

logger = logging.getLogger(__name__)

__REDIS_POOL = None

class Popper(object):
    def __init__(self, items):
        self.items = list(items)

    def pop(self, n):
        res = []
        for x in xrange(0, min(n, len(self.items))):
            res.append(self.items.pop())
        return res

def setup_redis():
    global __REDIS_POOL
    if not __REDIS_POOL:
        __REDIS_POOL = redis.ConnectionPool()
    r = redis.Redis(connection_pool=__REDIS_POOL)
    return r

def setup_queue(**kwargs):
    config = {
        'connection': os.getenv('RQ_CONNECTION', None), 
        'async': bool(os.getenv('RQ_ASYNC', False)),
    }
    config.update(kwargs)
    config['connection'] = setup_redis()
    return Queue(**config)

def setup_logging(logfile=None):
    shera_logger = logging.getLogger('shera')
    if logfile:
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        shera_logger.addHandler(hdlr)
    shera_logger.info('shera logger setup')
