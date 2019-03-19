# a. Main file: code for the proxy server
# b. Accompanying files:
#         1. cache.py: provides required classes for caching
#         2. parse.py: parses raw http requests
# c. variable MAX_CACHE_LIMIT defined in cache.py which limits no
#    of cache files
# d. implements caching, non_blocking parallel processing using threads
# e. default port, if not specified was assumed to be 80

import thread
import socket, os
import time

from cache import *
from parse import *

CRLF = "\r\n\r\n"

#create server and listen on port 12345
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.bind(("",12345))
c.listen(10)

#initiating cache engine
cached = CACHE()

#function to process http requests
#1. check if the file requested is cached
#2. if yes, query server with if-modified-since in header
#3. send from cache if not
#4. else forward response from server
def serve_client(s, a):
    request = s.recv(1024)
    m = http_params(request)
#check if cached
    cache = cached.check_if_cached(m["server"], m["port"], m["file"])[0]

    try:
        temp = ""
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        conn.connect((m["server"],m["port"]))
        
        if( cache ): # if cached
            conn.send("GET /%s\r\nIf-Modified-Since:%s%s" %(m["file"], cache.time, CRLF))
            data = conn.recv(1024)
            if( len(data) == 0 ): # and not modified since
                print "sending from cache"
                s.send(cache.data) # send from cache
                s.close()
                conn.shutdown(1)
                conn.close()
                return
            else:
                print "modified since cached"  # if modified send data received now
                s.send(data)
                temp += data
        else:
            print "not cached"
            conn.send("GET /%s%s" %(m["file"], CRLF)) # not cached, so normal request

        while True:
            data = conn.recv(1024)
            
            if (len(data) > 0):
                s.send(data)  #send remaining data
                temp += data
            else:
                cached.cache(m["server"], m["port"], m["file"], temp) #cache data
                conn.shutdown(1)
                conn.close()
                break
    except socket.error:
        print "connection error"
        s.send(ERROR_PAGE)

    s.close()

#provides non blocking connections
#each connection accepted is processed on a new thread
while True:
    s,a = c.accept()
    try:
        thread.start_new_thread(serve_client, (s, a))
    except:
        print error
    print ""

c.close()
