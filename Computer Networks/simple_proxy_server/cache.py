# a. Implements two classes:
#             1. CACHE_DATA: for each object cached
#             2. CACHE: manages cache data
# b. Data are cached according to the most recent requests
# c. No duplicate caching

from time import localtime, strftime
from datetime import datetime

MAX_CACHE_LIMIT = 3

class CACHE_DATA:
    ''' each cache object'''
    def __init__(self, server, port, filename, data):
         self.server = server
         self.port = port
         self.filename = filename
         self.data = data
         self.time = strftime('%a %b %d %H:%M:%S %Z %Y', localtime())

    def check(self, server, port, filename):
        if( self.server == server ):
            if( self.port == port ):
                if( self.filename == filename):
                    return True
        return False

class CACHE:
    ''' list of cache '''
    cached_data = []
    cache_len = 0
    cache_num = 0

    def check_if_cached(self, server, port, file_requested):
        for data in self.cached_data:
            if( data.check(server, port, file_requested) ):
                return [data, self.cached_data.index(data)]
        return [False, -1]

    def cache(self, server, port, filename, data):
        exists = self.check_if_cached(server, port, filename)
        if( exists[0] ):
            self.cached_data[exists[1]] = CACHE_DATA(server, port, filename, data)
        else:
            if( self.cache_len < MAX_CACHE_LIMIT - 1 ):
                self.cached_data.append(CACHE_DATA(server, port, filename, data))
            else:
                self.cached_data[self.cache_num] = CACHE_DATA(server, port, filename, data)
                self.cache_num = (self.cache_num + 1)%MAX_CACHE_LIMIT
        
