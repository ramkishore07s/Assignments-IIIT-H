import socket,os,errno

print('server_persistent.py')

#creating server:

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.bind(("",8080))
c.listen(10)
s,a = c.accept()

#get no. of files from client:
n = s.recv(10)
files = []
n = int(n,2)
print("n",n)

#get names of files req. from client:
for i in range (0, n):
	size = s.recv(10)
	size = int(size, 2)
	files.append(s.recv(size))

#send files as requested:
for i in range (0, n):
	print('file requested: ',files[i])
	if(os.path.isfile("Data/" + files[i])):
		file = open("Data/" + files[i], 'rb');
		s.send(bin(os.path.getsize("Data/" + files[i]))[2:].zfill(64))
		size = os.path.getsize("Data/" + files[i])
		print('file size', size)
		s.send(file.read(size))
		file.close()
		print('file sent')
	else:
		s.send(bin(0)[2:].zfill(16))
		print("file not found: ", files[i])
s.close()
c.close()
	
