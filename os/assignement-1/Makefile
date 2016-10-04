all: client1 server1

server1: server1.cpp
g++ -o s server1.cpp -pthread

client1: client1.cpp
g++ -o c client1.cpp

clean:

rm server1 client1
