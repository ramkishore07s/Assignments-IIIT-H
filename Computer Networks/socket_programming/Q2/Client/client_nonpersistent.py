import socket, sys, os

print("client_nonpersistent.py")
files = sys.argv[1:]
for i in files:
        #open socket connection for each file passed
        #as argument
	c = socket.socket()
	c.connect(("localhost", 8080))

        #send size of filename as 10 bit binary
	c.send(bin(len(i))[2:].zfill(10))
        #send name of file required
	c.send(i)

	print('file requested:',i)

        #receive size of file required
	size = c.recv(16)
	size = int(size,2)
	if size:
                print('file size:',size)
                file = open(i, 'w+')
                while(size > 0):
		        size -= 1024
		        file.write(c.recv(1024))
		file.close()
	print('file received')
	c.close()
