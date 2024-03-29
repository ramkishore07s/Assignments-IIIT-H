#include <errno.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/sendfile.h>
#define PORT 8080
char name[10][10];
int fileNo(char* buffer)
{
  int i = 0;
  for(i=0; i<3; ++i) 
    if(!strcmp(buffer, name[i]))
      return i;
  return -1;
}
	
int main(int argc, char const *argv[])
{
  int server_fd, new_socket, valread;
  struct sockaddr_in address;  // sockaddr_in - references elements of the socket address. "in" for internet
  int opt = 1;
  int addrlen = sizeof(address);
  char buffer[1024] = {0};
  char *hello = "Hello from server";

  // Creating socket file descriptor
  if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)  // creates socket, SOCK_STREAM is for TCP. SOCK_DGRAM for UDP
    {
      perror("socket failed");
      exit(EXIT_FAILURE);
    }

  // This is to lose the pesky "Address already in use" error message
  if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
		 &opt, sizeof(opt))) // SOL_SOCKET is the socket layer itself
    {
      perror("setsockopt");
      exit(EXIT_FAILURE);
    }
  address.sin_family = AF_INET;  // Address family. For IPv6, it's AF_INET6. 29 others exist like AF_UNIX etc. 
  address.sin_addr.s_addr = INADDR_ANY;  // Accept connections from any IP address - listens from all interfaces.
  address.sin_port = htons( PORT );    // Server port to open. Htons converts to Big Endian - Left to Right. RTL is Little Endian

  // Forcefully attaching socket to the port 8080
  if (bind(server_fd, (struct sockaddr *)&address,
	   sizeof(address))<0)
    {
      perror("bind failed");
      exit(EXIT_FAILURE);
    }

  // Port bind is done. You want to wait for incoming connections and handle them in some way.
  // The process is two step: first you listen(), then you accept()
  if (listen(server_fd, 3) < 0) // 3 is the maximum size of queue - connections you haven't accepted
    {
      perror("listen");
      exit(EXIT_FAILURE);
    }

  // returns a brand new socket file descriptor to use for this single accepted connection. Once done, use send and recv
  if ((new_socket = accept(server_fd, (struct sockaddr *)&address,
			   (socklen_t*)&addrlen))<0)
    {
      perror("accept");
      exit(EXIT_FAILURE);
    }
  char file_size[10];
  off_t offset;
  int sent, size_to_send, fd;
  struct stat info;
  int i;
  valread = read( new_socket, buffer, 10);
  int n = atoi(buffer), zero = 0;
  char names[10][10], z[10], act_names[10][20];
  char file[20] = "Data/";
  sprintf(z, "%d", zero);
  for(i=0; i<n; ++i) {
    valread = read( new_socket, buffer, 10);
    strcpy(file + 5, buffer);
    strcpy(act_names[i],file);
    strcpy(names[i], buffer);
  }
  for(i=0; i<n; ++i) {
    printf("loop %d\n", i);
    printf("file requested: %s\n", names[i]);
    fd=open(act_names[i], O_RDONLY);

    //file error handling
    if( fd == -1 ) {
      perror("File error");
      send(new_socket, z, 10, 0);
      continue;
    }
    if( fstat(fd, &info) < 0 ) {
      perror("File error");
      send(new_socket, z, 10, 0);
      continue;
    }

    //send file size
    sprintf(file_size, "%d", info.st_size);
    if ( send(new_socket, file_size, 10, 0) < 0 ) {
      printf("%s\n", strerror(errno));
      exit(EXIT_FAILURE);
    }

    //send file
    offset = 0;
    sent = 0;
    size_to_send = atoi(file_size);
    printf("%d\n",BUFSIZ);
    while(((sent = sendfile(new_socket, fd, &offset, 1024)) > 0) && (size_to_send>0)) {
      size_to_send -= sent;
      printf("sent: %d\n", sent);
    }
    printf("sent file: %s\n",name[i]);
    close(fd);
  }
  close(new_socket);
  close(server_fd);	
  return 0;
}
