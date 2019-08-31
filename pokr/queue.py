# -*- coding: utf-8 -*-

from builtins import object
import redis

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.db.blpop(self.key, timeout=timeout)
            if item:
                item = item[1]
        else:
            item = self.db.lpop(self.key)

        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def __iter__(self):
        return self

    def __next__(self):
        item = self.get(False)
        if item is None:
            raise StopIteration
        return item
