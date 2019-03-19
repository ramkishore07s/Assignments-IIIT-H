// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <arpa/inet.h>
#define PORT 8080

int main(int argc, char const *argv[])
{
    struct sockaddr_in address;
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char *hello = "Hello from client";
    char buffer[1024] = {0};
	char name[][10] = {"file1.txt", "files.txt", "file3.txt"};
	int j;
//	for(j=1; j<argc; ++j) {
//		strcpy(name[j-1], argv[j]);
//		printf("%d\n",j);

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }

    memset(&serv_addr, '0', sizeof(serv_addr)); // to make sure the struct is empty. Essentially sets sin_zero as 0
                                                // which is meant to be, and rest is defined below

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Converts an IP address in numbers-and-dots notation into either a 
    // struct in_addr or a struct in6_addr depending on whether you specify AF_INET or AF_INET6.
    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)  // connect to the server address
    {
        printf("\nConnection Failed \n");
        return -1;
    }
int n, i, rest, file_size, remaining;
ssize_t rate;
FILE* rec;

//n = argc -1;
n = 3;

char number[10];
sprintf(number, "%d", n);
send(sock, number, 10, 0);
for(i=0; i<n; ++i)
	send(sock, name[i], 10, 0);
for(i=0; i<n; ++i) {
	remaining = 1024;
	rec = fopen(name[i], "w");
       // send(sock , name[i] , strlen(name[i]) , 0 );  // send the message.
 	printf("file requested: %s\n", name[i]);
	valread = read( sock , buffer, 10);  // receive message back from server, into the buffer
	printf("file size: %s\n",buffer );
	file_size = atoi(buffer);
	rest = file_size;
	if( file_size > 0 ) {
	while(( (rate = recv(sock, buffer, remaining, 0)) > 0) && rest > 0) {
		fwrite(buffer, sizeof(char), rate, rec);
		rest -= rate;
		printf("received: %d bytes rest: %d bytes\n", rate, rest);
		if( rest < remaining )
			remaining = rest;
	}
}
	fclose(rec);
	printf("received file %s\n", name[i]);
}

	close(sock);	
    return 0;
}
