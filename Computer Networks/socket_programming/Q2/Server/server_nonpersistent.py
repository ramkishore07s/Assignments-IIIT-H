import socket,os

print('server_nonpersistent.py')


#create server and listen on port 8080
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.bind(("",8080))
c.listen(10)



while True:
        #accept multiple connections, although serially
	s,a = c.accept()

        #receive binary encoded size
	size = s.recv(10)
	size = int(size, 2)
	f = s.recv(size)
	print('file requested: ',f)

        #check if file exists and proceed
	if(os.path.isfile("Data/" + f)):
		file = open("Data/" + f, 'rb');
		s.send(bin(os.path.getsize("Data/" + f))[2:].zfill(16))
		size = os.path.getsize("Data/" + f)
		print('file size', size)
		s.send(file.read(size))
		file.close()
		print('file sent')
	else:
		s.send(bin(0)[2:].zfill(16))
		print("file not found: ", f)
s.close()
c.close()
	
