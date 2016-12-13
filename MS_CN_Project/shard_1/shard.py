import socket
import sys
import json
import os
import base64
import fileinput
import gzip
import shutil

if len(sys.argv) < 3:
    print 'python shard1.py -config [configuration file name]'
    exit()

arg_1 = sys.argv[1]
arg_2 = sys.argv[2] 

if arg_1 == '-config':
    with open(arg_2) as con_file:
        data = json.load(con_file)

label = 1
host =''

print 'reading configuration information from json file'
print 'homrdir      ', data["homedir"]
print 'shard1ip ', data["shard1ip"]
print 'shard1port   ', data["shard1port"]
print 'shard2ip ', data["shard2ip"]
print 'shard2port   ', data["shard2port"]

def file_size(filename):
        st = os.stat(filename)
        return st.st_size

def rec_client(sock, recv_buffer=1024, delim='}'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data

        if buffer.find(delim) != -1:
            yield buffer
            return

def upload_file(filename):
    f = open(filename,'w+')
    f.write(base64.b64decode(json_obj['Data']))
    f.close()
    print 'File saved'

def backup_shard2(size):
    if size % 2 != 0:
        to_shard2 = size/2 + 1
    else:
        to_shard2 = size/2
    return to_shard2



server_address1 = (data["shard1ip"], int(data["shard1port"]))
server_address2 = (data["shard2ip"], int(data["shard2port"]))
server_address = (host, int(data["listenport"]))
print >>sys.stderr, 'starting up on %s port %s' % server_address

# Creating a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)

while True:
    # Wait for a connection
    print '***Waiting for client requests***'
    connection, client_address = sock.accept()
    print 'Connection from', client_address
    byte_ask = ''
    for buffer in rec_client(connection):
        byte_ask = buffer
    json_obj = json.loads(byte_ask)
    if json_obj['MessageType'] == 'BYTESTORED':
        print 'Client asking Bytes stored'
        f = open(data["metadatafile"],'r+')
        line = f.readline()
        byte_tell = {'MessageType': 'BYTESTORED', 'BytesStored': str(int(line))}
        encoded_msg = json.dumps(byte_tell)
        while encoded_msg:
            bytes = connection.send(encoded_msg)
            encoded_msg = encoded_msg[bytes:]

        print 'Reply was ' + str(int(line)) + ' bytes'

        try:
            byte_ask = ''
            for buffer in rec_client(connection):
                byte_ask = buffer
            json_obj = json.loads(byte_ask)
        except Exception, e:
                print str(e)
                continue

        print 'Received upload request of ' + str(int((int(json_obj['BytesTo']) - int(json_obj['BytesFrom'])))) + ' bytes for ' + json_obj['Filename']

        if json_obj['MessageType'] == 'DATA':
            upload_file(json_obj['Filename']);
            confirm = {'MessageType': 'Message', 'Content': 'Done'}
            encoded_msg = json.dumps(confirm)
            while encoded_msg:
                bytes = connection.send(encoded_msg)
                encoded_msg = encoded_msg[bytes:]

            with open(data["metadatafile"],'r') as file:
                file_contents = file.readlines()
                size = file_size(json_obj['Filename'])
                meta_size = int(file_contents[0])
                meta_size += size
                file_contents[0] = str(meta_size)+'\n'

            with open(data["metadatafile"],'w') as file:
                file.writelines( file_contents )
            with open(data["metadatafile"],'a') as file:
                file.write(json_obj['Filename']+'\n'+str(size)+'\n'+json_obj['BytesFrom']+'\n'+json_obj['BytesTo']+'\n')
            sock1.connect(server_address1)
            sock2.connect(server_address2)
            f = open(json_obj['Filename'],'r+')
            size = file_size(json_obj['Filename'])
            to_shard1 = size/2
            to_shard2 = backup_shard2(size)


            msg_to_send1 = {'MessageType': 'BACKUPDATA', 'Filename': str(json_obj['Filename']), 'BytesFrom': json_obj['BytesFrom'], 'BytesTo': str(int(json_obj['BytesFrom'])+to_shard1 - 1), 'Data': base64.b64encode(str(f.read(to_shard1)))}
            msg_to_send2 = {'MessageType': 'BACKUPDATA', 'Filename': str(json_obj['Filename']), 'BytesFrom': str(int(json_obj['BytesFrom'])+to_shard1), 'BytesTo': str(int(json_obj['BytesFrom'])+to_shard1 + to_shard2 - 1), 'Data': base64.b64encode(str(f.read(to_shard2)))}
            encoded_msg1 = json.dumps(msg_to_send1)
            encoded_msg2 = json.dumps(msg_to_send2)
            while encoded_msg1:
                bytes = sock1.send(encoded_msg1)
                encoded_msg1 = encoded_msg1[bytes:]
            print 'Backup sent to shard 1'

            while encoded_msg2:
                bytes = sock2.send(encoded_msg2)
                encoded_msg2 = encoded_msg2[bytes:]
            print 'Backup sent to shard 2'

            sock1.close()
            sock2.close()
            

    elif json_obj['MessageType'] == 'BACKUPDATA':
        f = open(str('backup'+str(label)+json_obj['Filename']),'w+')
        f.write(base64.b64decode(json_obj['Data']))
        #zip backup
        f.close()
        
        with open(data["metadatafile"],'r') as file:
            file_contents = file.readlines()
        size = file_size(str('backup'+str(label)+json_obj['Filename']))
        meta_size = int(file_contents[0])
        meta_size += size
        file_contents[0] = str(meta_size)+'\n'

        with open(data["metadatafile"],'w') as file:
            file.writelines( file_contents )

        with open(data["metadatafile"],'a') as file:
            file.write(str('backup'+str(label)+json_obj['Filename'])+'\n'+str(size)+'\n'+json_obj['BytesFrom']+'\n'+json_obj['BytesTo']+'\n')
        label = label+1;
        

    elif json_obj['MessageType'] == 'FILEINFO':
        print 'Client wants to download a file '
        with open(data["metadatafile"],'r') as file:
            file_contents = file.readlines()

        i = 1
        file_on_shard = 0
        while file_contents[i:]:
            if file_contents[i] == str(json_obj['Filename']+'\n'):
                file_on_shard = 0
                break
            else:
                file_on_shard = 1
            i+= 4

        if file_on_shard == 1:
            print 'No such file exists'
        else:
            BytesF2 = str(int(file_contents[i+6]))
            BytesT2 = str(int(file_contents[i+7]))
            BytesF3 = str(int(file_contents[i+10]))
            BytesT3 = str(int(file_contents[i+11]))
            if BytesF3 < BytesF2:
                temp1 = BytesF3
                temp2 = BytesT3
                BytesF3 = BytesF2
                BytesT3 = BytesT2
                BytesF2 = temp1
                BytesT2 = temp2

            msg_to_send = {'MessageType': 'FILEINFO', 'Filename': str(json_obj['Filename']), 'BytesFrom': str(int(file_contents[i+2])), 'BytesTo': str(int(file_contents[i+3])), 'BytesFrom2': BytesF2, 'BytesTo2': BytesT2, 'BytesFrom3': BytesF3, 'BytesTo3': BytesT3}
            encoded_msg = json.dumps(msg_to_send)
            print 'sending FILEINFO for ' + json_obj['Filename']
            while encoded_msg:
                bytes = connection.send(encoded_msg)
                encoded_msg = encoded_msg[bytes:]
            byte_ask = ''
            for buffer in rec_client(connection):
                byte_ask = buffer
            json_obj = json.loads(byte_ask)
            print 'Client wants file ' + json_obj['Filename']
            if json_obj['MessageType'] == 'REQUESTDATA':
                f = open(json_obj['Filename'],'r+')
                msg_to_send = {'MessageType': 'DATA', 'Filename': str(json_obj['Filename']), 'BytesFrom': json_obj['BytesFrom'], 'BytesTo': json_obj['BytesTo'], 'Data': base64.b64encode(str(f.read()))}
                encoded_msg = json.dumps(msg_to_send)
            while encoded_msg:
                bytes = connection.send(encoded_msg)
                encoded_msg = encoded_msg[bytes:]
            print 'File sent'
            byte_ask = ''
            for buffer in rec_client(connection):
                byte_ask = buffer
            try:
                json_obj = json.loads(byte_ask)
            except Exception, e:
                continue
            print json_obj['MessageType']
            if json_obj['MessageType'] == 'REQUESTDATA':
                with open(data["metadatafile"],'r') as file:
                    file_contents = file.readlines()
                    i = 1
                    file_on_shard = 0
                    while file_contents[i:]:
                        if file_contents[i] == str(json_obj['Filename']+'\n'):
                            file_on_shard = 0
                            break
                        else:
                            file_on_shard = 1
                        i+= 4
                    if  int(json_obj['BytesFrom']) == int(file_contents[i+6]) and int(json_obj['BytesTo']) == int(file_contents[i+7]):
                        f = open(str(file_contents[i+4]).rstrip(),'r+')
                        msg_to_send = {'MessageType': 'DATA', 'Filename': str(json_obj['Filename']), 'BytesFrom': json_obj['BytesFrom'], 'BytesTo': json_obj['BytesTo'], 'Data': base64.b64encode(str(f.read()))}
                        encoded_msg = json.dumps(msg_to_send)
                        while encoded_msg:
                            bytes = connection.send(encoded_msg)
                            encoded_msg = encoded_msg[bytes:]
                        print 'Backup sent'
                    elif int(json_obj['BytesFrom']) == int(file_contents[i+10]) and int(json_obj['BytesTo']) == int(file_contents[i+11]):
                        f = open(str(file_contents[i+8]).rstrip(),'r+')
                        msg_to_send = {'MessageType': 'DATA', 'Filename': str(json_obj['Filename']), 'BytesFrom': json_obj['BytesFrom'], 'BytesTo': json_obj['BytesTo'], 'Data': base64.b64encode(str(f.read()))}
                        encoded_msg = json.dumps(msg_to_send)
                        while encoded_msg:
                            bytes = connection.send(encoded_msg)
                            encoded_msg = encoded_msg[bytes:]
                        print 'Backup sent'

