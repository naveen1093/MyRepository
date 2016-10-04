/**
$saikiran goud burra
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>    //strlen
#include <sys/socket.h>
#include <arpa/inet.h> //inet_addr
#include <unistd.h>    //usleep
#include <fcntl.h> //fcntl
#include <sys/time.h>
#include <time.h>
#include <netdb.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <iostream>
#include <pthread.h>
#include <algorithm>

using namespace std;
int resource[32] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32};
int lock_indicator[32] ={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; // creat lock is 1, read lock 2, write lock 3

void *connection_handler(void *socket_desc)
{
    //Get the socket descriptor
    int sock = *(int*)socket_desc;
    int read_size, client_request;
    const char *message ;
    char client_message[20];
     
    //Send some messages to the client     
    //Receive a message from client
    while( (read_size = recv(sock , client_message , 2000 , 0)) > 0 )
    {
        //Send the message back to client
    	//perform operations 
        //write(sock , client_message , strlen(client_message));
		cout<<client_message<<"\n";
		if(client_message[0]=='C' && client_message[1]=='L')
		{
			//extract resource and create lock
			client_request=client_message[3];
			int x = distance(resource, find(resource, resource + 32, client_request));
			if(lock_indicator[x]==0){
				lock_indicator[x]=1;
				message= "created lock for resource \n";
				write(sock , message , strlen(message));
			}
			else{
				message = "cannot creat lock as it already created a lock \n";
				write(sock , message , strlen(message));
			}
		}
		if(client_message[0]=='R' && client_message[1]=='L')
		{
			//extract resource and create lock
			client_request=client_message[3];
			int x = distance(resource, find(resource, resource + 32, client_request));
			if(lock_indicator[x]==1 || lock_indicator[x]==2){
				lock_indicator[x]=2;
				message = "successfully read lock done \n";
				write(sock , message , strlen(message));
			}
			else{
				message = "cannot read \n";
				write(sock , message , strlen(message));
			}
		}
		if(client_message[0]=='W' && client_message[1]=='L')
		{
			//extract resource and create lock
			client_request=client_message[3];
			int x = distance(resource, find(resource, resource + 32, client_request));
			if(lock_indicator[x]==1){
				lock_indicator[x]=3;
				message = "writing lock successfully done\n";
				write(sock , message , strlen(message));
			}
			else{
				message = "cannot write \n";
				write(sock , message , strlen(message));
			}
		}
		if(client_message[0]=='R' && client_message[1]=='U')
		{
			//extract resource and create lock
			client_request=client_message[3];
			int x = distance(resource, find(resource, resource + 32, client_request));
			if(lock_indicator[x]==2){
				lock_indicator[x]=1;
			}
		}
		if(client_message[0]=='W' && client_message[1]=='U')
		{
			//extract resource and create lock
			client_request=client_message[3];
			int x = distance(resource, find(resource, resource + 32, client_request));
			if(lock_indicator[x]==3){
				lock_indicator[x]=1;
			}
		}
		if(client_message[0]=='D' && client_message[1]=='L')
		{
			//extract resource and create lock
			client_request=client_message[3];
			int x = distance(resource, find(resource, resource + 32, client_request));
			if(lock_indicator[x]==1){
				lock_indicator[x]=0;
				message= "successfully deleted lock \n";
				write(sock , message , strlen(message));
			}
			else{
				message = "cannot delete because some one has read or write lock \n";
				write(sock , message , strlen(message));
			}
		}
		if(client_message[0]=='K' && client_message[1]=='S')
		{
			shutdown(sock, 2);
		}
    }
     
   /* if(read_size == 0)
    {
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
    {
        perror("recv failed");
    } */
         
    //Free the socket pointer
    free(socket_desc);
     
    return 0;
}

int main()
{
	int socket_desc , client_sock, c , *new_sock;
	struct sockaddr_in server , client;
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons( 20001 );
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        //print the error message
        perror("bind failed. Error");
        return 1;
    }
    listen(socket_desc , 3);
    c = sizeof(struct sockaddr_in);
    while( (client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
    {
        puts("Connection accepted");
         
        pthread_t sniffer_thread;
        new_sock = static_cast<int*>(malloc(1));
        *new_sock = client_sock;
         
        if( pthread_create( &sniffer_thread , NULL ,  connection_handler , (void*) new_sock) < 0)
        {
            perror("could not create thread");
            return 1;
        }
         
        //Now join the thread , so that we dont terminate before the thread
        //pthread_join( sniffer_thread , NULL);
        //puts("Handler assigned");
    }
     
    if (client_sock < 0)
    {
        perror("accept failed");
        return 1;
    }
     
    return 0;
}

