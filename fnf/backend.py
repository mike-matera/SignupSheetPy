import pickle
from django.core.cache.backends.memcached import BaseMemcachedCache

class GaeMemcachedCache(BaseMemcachedCache):
    "An implementation of a cache binding using google's app engine memcache lib (compatible with python-memcached)"
    def __init__(self, server, params):
        from google.appengine.api import memcache
        super(GaeMemcachedCache, self).__init__(server, params,
                                             library=memcache,
                                             value_not_found_exception=ValueError)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = self._lib.Client(self._servers, pickleProtocol=pickle.HIGHEST_PROTOCOL)
        return self._client

#    def make_key(self, key, version=None):
#        key = super(GaeMemcachedCache, self).make_key(key, version)
#        print "Made key:", key
#        return key
