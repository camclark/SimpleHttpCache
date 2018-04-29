"""
 ~~ Overview ~~ 
Implement a simple online cache to store documents of the form:
{
 “id”: int,
 “message”: string
}
- id is the unique identifier for the document.
- message is the body of the document and can be any string
An example of a well formed message:
{
 “id”: 2019,
 “message”: “Telstra 2019 Graduate Program”
}

Your cache must be able to store and retrieve documents through a RESTful API that it exposes, as outlined below. The internal
implementation of the cache, including implementation language, as well as any design choices such as how documents are
stored, are at your own discretion

"""

import datetime


class SimpleCache:

    def __init__(self):
        # TODO: have a 30 second TTL
        self.cache = {}
        self.max_cache_size = 10

    def __contains__(self, k):
        """
        Returns True or False if key in cache
        """
        return k in self.cache

    def get(self, k):
        """
        Get contents of key if in cache
        """
        if k in self.cache:
            return self.cache[k]['value']

    def update(self, k, v):
        """
        Update the cache dictionary if required remove the oldest item
        """

        # remove last item if cache is full
        if k not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()

        self.cache[k] = {'date_accessed': datetime.datetime.now(), 'value': v}

    def ttl_check(self):
        for k in self.cache:
            if self.cache[k]['date_accessed'] < datetime.datetime.now() - datetime.timedelta(seconds=30):
                self.cache.pop(k)

    def remove_oldest(self):
        """
        Remove the entry that has the oldest accessed date
        """
        oldest_entry = None

        for k in self.cache:
            if oldest_entry is None:
                oldest_entry = k
            elif self.cache[k]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = k
        self.cache.pop(oldest_entry)



    @property
    def size(self):
        """
        Return the size of the cache
        """
        return len(self.cache)


if __name__ == '__main__':
    # Test the cache ints 2000 to 2020
    keys = [i for i in range(2000, 2020)]
    s = "string"
    cache = SimpleCache()
    for i, key in enumerate(keys):
        if key not in cache:
            value = s
            cache.update(key, value)
        print("#%s iterations, #%s cached entries, value: %s" % (i+1, cache.size, cache.get(key)))
    print()

    while True:
        cache.ttl_check()

    # should delete nothing



