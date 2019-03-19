import socket, sys, os

#open one socket connection for all files:
print('client_persistent.py')

c = socket.socket()
c.connect(("localhost", 8080))

#send no. of files in 10 bit binary encoding:
c.send(bin(len(sys.argv[1:]))[2:].zfill(10))
files = sys.argv[1:]
print(len(files))

#send names of files required:
for i in sys.argv[1:]:
	c.send(bin(len(i))[2:].zfill(10))
	c.send(i)

#get files from server:
for i in files:
	print('file requested:',i)
	size = c.recv(64)
	size = int(size,2)
        if size:
                file = open(i,'w+')
                print('file size:',size)
                file.write(c.recv(size))
	        file.close()
	print('file received')
c.close()
