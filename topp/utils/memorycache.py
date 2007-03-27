"""
Simple memory cache.

Usage::

    >>> def callit(arg):
    ...     print 'Calculating', arg
    ...     return arg + 1
    >>> callit(1)
    Calculating 1
    2
    >>> callit(1)
    Calculating 1
    2
    >>> callit = cache()(callit)
    >>> callit(1)
    Calculating 1
    2
    >>> callit(1)
    2
    >>> callit.cache.expire_all()
    >>> callit(1)
    Calculating 1
    2

This cache is slightly sloppy, and may call the decorated function
more than necessary when concurrently accessed from different threads.
It prefers less locking and less possible deadlocks to avoiding
function calls.
"""

import threading
import time

class Cache(object):

    """
    Caches objects in memory.  Keeps objects for `expire` seconds
    (default 10 minutes), though objects may persist somewhat longer.
    """

    def __init__(self, expire=600):
        self.expire = expire
        self.objects = {}
        self._lock = threading.Lock()
        self._last_checked = time.time()

    def get_object(self, key):
        """
        Returns the keyed object, or raises
        KeyError
        """
        self._check_expire()
        created, obj = self.objects[key]
        if time.time() - created > self.expire:
            try:
                del self.objects[key]
            except KeyError:
                pass
            raise KeyError(key)
        return obj

    def set_object(self, key, value):
        """
        Sets the object for the key
        """
        self._check_expire()
        self.objects[key] = (time.time(), value)

    def expire_all(self):
        self._lock.acquire()
        try:
            self.objects.clear()
        finally:
            self._lock.release()

    def _check_expire(self):
        now = time.time()
        if now - self._last_checked < self.expire*2:
            return
        acquired = self._lock.acquire(False)
        if not acquired:
            # Someone else is expiring stuff, so
            # we don't need to
            return
        try:
            for key in self.objects.keys():
                if now-self.objects[key][0] > self.expire:
                    try:
                        del self.objects[key]
                    except KeyError:
                        pass
        finally:
            self._lock.release()

def cache(expire=600):
    """
    Decorate a function with this to cache the output of the function,
    keyed off the positional arguments passed into the function.  The
    positional arguments must be hashable (e.g., no dicts)x, and no
    keyword arguments are allowed.
    """
    def decorator(func):
        return CachedFunc(func, expire=expire)
    return decorator

class CachedFunc(object):

    def __init__(self, func, expire):
        self.cache = Cache(expire=expire)
        self.func = func

    def __call__(self, *args):
        try:
            return self.cache.get_object(args)
        except KeyError:
            value = self.func(*args)
            self.cache.set_object(args, value)
            return value

    def __repr__(self):
        return '<%s %s expire=%r around %s>' % (
            self.__class__.__name__,
            hex(id(self)), self.cache.expire,
            repr(self.func)[1:-1])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
