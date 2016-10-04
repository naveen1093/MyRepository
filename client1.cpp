/**
$saikiran goud burra
*/
// Obligatory includes
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

using namespace std;

// Constants
#define ALPHA 0
#define BRAVO 5


// Templates to be filled
int create_lock(int resource)
{
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "CL";
	snprintf(temp, sizeof(temp), "_%d", resource);
	//cout<<"debug1 \n";
	strcat(messsage,messsage1);
	//cout<<"debug2 \n";
	strcat(messsage,temp);
	//cout<<"debug3 \n";
	sock = socket(AF_INET , SOCK_STREAM , 0);
	//cout<<"debug4 \n";
	if (sock == -1)
    {
        cout<<"Could not create socket \n";
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		//cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		//cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		//cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } 
	puts(server_reply);
	return 0;
}
int read_lock(int resource)
{  
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "RL";
	snprintf(temp, sizeof(temp), "_%d", resource);
	strcat(messsage,messsage1);
	strcat(messsage,temp);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1)
    {
        printf("Could not create socket");
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } 
	puts(server_reply);
	return 0; 
}
int write_lock(int resource)
{
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "WL";
	snprintf(temp, sizeof(temp), "_%d", resource);
	strcat(messsage,messsage1);
	strcat(messsage,temp);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1)
    {
        printf("Could not create socket");
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } 
	puts(server_reply);
	return 0;   
}
int read_unlock(int resource)
{
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "RU";
	snprintf(temp, sizeof(temp), "_%d", resource);
	strcat(messsage,messsage1);
	strcat(messsage,temp);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1)
    {
        printf("Could not create socket");
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    /*if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } */
	return 0;
}
int write_unlock(int resource)
{   
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "WU";
	snprintf(temp, sizeof(temp), "_%d", resource);
	strcat(messsage,messsage1);
	strcat(messsage,temp);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1)
    {
        printf("Could not create socket");
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    /*if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } */
	return 0;
}
int delete_lock(int resource)
{   
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "DL";
	snprintf(temp, sizeof(temp), "_%d", resource);
	strcat(messsage,messsage1);
	strcat(messsage,temp);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1)
    {
        printf("Could not create socket");
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } 
	puts(server_reply);
	return 0;
}
int kill_server()
{   
	int sock;
	struct sockaddr_in server;
	char *temp = (char*)malloc(100);
	char *messsage = (char*)malloc(100);
	char *server_reply = (char*)malloc(100);
	const char *messsage1 = "KS";
	strcat(messsage,messsage1);
	strcat(messsage,temp);
	sock = socket(AF_INET , SOCK_STREAM , 0);
	if (sock == -1)
    {
        printf("Could not create socket");
    }
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 20001 );
    if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
		cout<<"debug5 \n";
        std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    if( send(sock , messsage , strlen( messsage ) , 0) < 0)
    {
		cout<<"debug6 \n";
        puts("Send failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 1;
    }
    /*if( recv(sock , server_reply , 2000 , 0) < 0)
    {
		cout<<"debug7 \n";
        puts("recv failed");
		std::cerr << "Error: " << strerror(errno) << std::endl;
        return 0;
    } */
	close(sock);
	return 0;
}

main () {
	int pid; // child's pid

        // Before the fork
        cout << "Create lock ALPHA\n";
	create_lock(ALPHA);
        cout << "Create lock BRAVO\n";
	create_lock(BRAVO);
        cout << "Parent requests write permission on lock BRAVO\n";
	write_lock(BRAVO);
        cout << "Write permission on lock BRAVO was granted\n";
        cout << "Parent requests read permission on lock ALPHA\n";
	read_lock(ALPHA);
        cout << "Read permission on lock ALPHA was granted\n";
	sleep(1);
	
	// Fork a child
	if ((pid = fork()) == 0) {
		// Child process
	        cout << "Child requests read permission on lock ALPHA\n";
		read_lock(ALPHA); // This permission should be granted
        	cout << "Read permission on lock ALPHA was granted\n";
		sleep(1);
	        cout << "Child releases read permission on lock ALPHA\n";
		read_unlock(ALPHA);
		sleep(1);
        	cout << "Child requests write permission on lock BRAVO\n";
		write_lock(BRAVO); // Should wait until parent relases its lock
        	cout << "Write permission on lock BRAVO was granted\n";
		sleep(1);
	        cout << "Child releases write permission on lock BRAVO\n";
		write_unlock(BRAVO);
		cout << "Child terminates\n";
                _exit(0);
	} // Child

	// Back to parent
        cout << "Parent releases read permission on lock ALPHA\n";
	read_unlock(ALPHA);
        cout << "Parent requests write permission on lock ALPHA\n";
	write_lock(ALPHA); // Should wait until child removes its read lock
        cout << "Write permission on lock ALPHA was granted\n";
	sleep(1);
        cout << "Parent releases read permission on lock ALPHA\n";
	read_unlock(ALPHA);
	sleep(1);
        cout << "Parent releases write permission on lock BRAVO\n";
	write_unlock(BRAVO);

	// Child and parent join
        while (pid != wait(0));  // Busy wait
	delete_lock(ALPHA);
        delete_lock(BRAVO);
        // We assume that failed operations return a non-zero value
        if (write_lock(ALPHA) != 0) {
		cout << "Tried to access a deleted lock\n";
	}
	kill_server();
} // main
	
