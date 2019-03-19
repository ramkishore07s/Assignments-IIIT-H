# a. Implements http_params for a simple raw http request.
# b. ERROR_PAGE is returned when this proxy server is unable
#    to contact the requested server.

DEFAULT_PORT = 80
ERROR_PAGE = '''<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Error code 502.
<p>Message: Bad Gateway.
<p>Error code explanation: 502 = No response from server.
</body>
'''

def http_params(request):
    firstLine = request.split('\n')[0]
    url = firstLine.split(' ')[1]

    domain_pos = url.find('://')
    server = url[domain_pos+ 3:].split('/')[0]

    file_requested = ""
    try:
        file_requested = url[domain_pos + 3:].split('/')[1]
        print "file:"+file_requested
    except:
        pass
    
    port_pos = server.find(":")
    if( port_pos == -1 ):
        port = DEFAULT_PORT
    else:
        port = int(server[port_pos+1:])
    print "server:"+server
    print "port:"+str(port)

    if(( server.find('localhost') != -1) or (server.find('127.0.0.1') != -1)):
        server = ""

    return {"server":server, "port":port,"file":file_requested}

