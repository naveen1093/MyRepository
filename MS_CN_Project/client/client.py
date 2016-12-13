import socket
import sys
import os
import json
import base64
import fileinput

#commandline arguments
if len(sys.argv) < 5:
	print 'python client.py -config [configuration file name] -[upload/download] [name of file to upload/download]'
	exit()

Download = 0;
Upload = 0;
File = ''
Connected1 = 0
Connected2 = 0
Connected3 = 0
Connected_to_all = 0

arg_1 = sys.argv[1] 
arg_2 = sys.argv[2] 
arg_3 = sys.argv[3] 
arg_4 = sys.argv[4]

if arg_1 == '-config':
	with open(arg_2) as con_file:
		data = json.load(con_file)


if arg_3 == '-upload':
        File = arg_4
	Upload = 1

if arg_3 == '-download':
        File = arg_4
	Download = 1


print 'reading configuration information from json file'
print 'homrdir	', data["homedir"]
print 'shard1ip ', data["shard1ip"]
print 'shard1port ', data["shard1port"]


def file_size(filename):
        st = os.stat(filename)
        return st.st_size

def rec_shard(sock, recv_buffer=1024, delim='}'):
	buffer = ''
	data = True
	while data:
		data = sock.recv(recv_buffer)
		buffer += data

		if buffer.find(delim) != -1:
			yield buffer
			return
	
def balance_load(total_bytes,shard_bytes):
	balance=total_bytes-shard_bytes
	return balance



#open sockets
server_address = (data["shard1ip"], int(data["shard1port"]))
server_address1 = (data["shard2ip"], int(data["shard2port"]))
server_address2 = (data["shard3ip"], int(data["shard3port"]))
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#shard connections
try:
	sock.connect(server_address)
	print 'connected to shard 1 at ip ' + data["shard1ip"] + 'and port ' + data["shard1port"]
	Connected1 = 1
except Exception, e:
	Connected1 = 0
try:
	sock1.connect(server_address1)
	print 'connected to shard 2 at ip ' + data["shard2ip"] + 'and port ' + data["shard2port"]
	Connected2 = 1
except Exception, e:
	Connected2 = 0
try:
	sock2.connect(server_address2)
	print 'connected to shard 3 at ip ' + data["shard3ip"] + 'and port ' + data["shard3port"]
	Connected3 = 1
except Exception, e:
	Connected3 = 0

if Connected1 == 1 and Connected2 == 1 and Connected3 ==1:
	Connected_to_all = 1



if Download == 1:
        file_to_download = {'MessageType': 'FILEINFO', 'Filename': str(File)}
	encoded_msg= json.dumps(file_to_download)

	print 'asking if shards have the file'
	while encoded_msg:
		if Connected1 == 1:
			bytes = sock.send(encoded_msg)
		if Connected2 == 1:
			bytes = sock1.send(encoded_msg)
		if Connected3 == 1:
			bytes = sock2.send(encoded_msg)
		encoded_msg = encoded_msg[bytes:]
	file_download1 = ''
	file_download2 = ''
	file_download3 = ''
	# Receive the data in small chunks and retransmit it
	if Connected1 == 1:
		for buffer in rec_shard(sock):
			file_download1 = buffer
		json1 = json.loads(file_download1)
		print 'File is present from ' + json1['BytesFrom'] + ' to ' + json1['BytesTo']

	if Connected2 == 1:
		for buffer in rec_shard(sock1):
			file_download2 = buffer
		json2 = json.loads(file_download2)
		print 'File is present from ' + json2['BytesFrom'] + ' to ' + json2['BytesTo']

	if Connected3 == 1:
		for buffer in rec_shard(sock2):
			file_download3 = buffer
		json3 = json.loads(file_download3)
		print 'File is present from ' + json3['BytesFrom'] + ' to ' + json3['BytesTo']
	
	if Connected1 == 1:
		file_send1 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json1['BytesFrom'], 'BytesTo': json1['BytesTo']}
		encoded_msg1 = json.dumps(file_send1)
		while encoded_msg1:
			bytes = sock.send(encoded_msg1)
			encoded_msg1 = encoded_msg1[bytes:]

	if Connected2 == 1:
		file_send2 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json2['BytesFrom'], 'BytesTo': json2['BytesTo']}
		encoded_msg2 = json.dumps(file_send2)
		while encoded_msg2:
			bytes = sock1.send(encoded_msg2)
			encoded_msg2 = encoded_msg2[bytes:]

	if Connected3 == 1:
		file_send3 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json3['BytesFrom'], 'BytesTo': json3['BytesTo']}
		encoded_msg3 = json.dumps(file_send3)
		while encoded_msg3:
			bytes = sock2.send(encoded_msg3)
			encoded_msg3 = encoded_msg3[bytes:]

	file_data1 = ''
	file_data2 = ''
	file_data3 = ''
	#all shards alive
	if Connected_to_all == 1:
		for buffer in rec_shard(sock):
			file_data1 = buffer
			json_1 = json.loads(file_data1)
		for buffer in rec_shard(sock1):
			file_data2 = buffer
			json_2 = json.loads(file_data2)
		for buffer in rec_shard(sock2):
			file_data3 = buffer
			json_3 = json.loads(file_data3)
		if json_1['MessageType'] == 'DATA' and json_2['MessageType'] == 'DATA' and json_3['MessageType'] == 'DATA':
			f = open(json_1['Filename'],'w+')
			f.write(base64.b64decode(json_1['Data']))
			f.write(base64.b64decode(json_2['Data']))
			f.write(base64.b64decode(json_3['Data']))
			f.close()
			print 'downloaded the file ' + json_1['Filename'] + 'from primary storage of all shards'

	#shard 3 is dead
	elif Connected1 == 1 and Connected2 == 1:
		#download primary bytes from shard 1 and shard 2
		for buffer in rec_shard(sock):
			file_data1 = buffer
			json_1 = json.loads(file_data1)
		for buffer in rec_shard(sock1):
			file_data2 = buffer
			json_2 = json.loads(file_data2)
		#download backup bytes from shard 1
		msg_send1 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json1['BytesFrom3'], 'BytesTo': json1['BytesTo3']}
		backup_req1 = json.dumps(msg_send1)
		print backup_req1
		while backup_req1:
			bytes = sock.send(backup_req1)
			backup_req1 = backup_req1[bytes:]
		backup_data1 = ''
		for buffer in rec_shard(sock):
			backup_data1 = buffer
		json_backup1 = json.loads(backup_data1)
		#download backup bytes from shard 2
		msg_send2 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json2['BytesFrom3'], 'BytesTo': json2['BytesTo3']}
		backup_req2 = json.dumps(msg_send2)
		while backup_req2:
			bytes = sock1.send(backup_req2)
			backup_req2 = backup_req2[bytes:]
		backup_data2 = ''
		for buffer in rec_shard(sock1):
			backup_data2 = buffer
		json_backup2 = json.loads(backup_data2)
		#assemble data, write to file in correct order
		file_with_backup = open(json_1['Filename'],'w+')
		file_with_backup.write(base64.b64decode(json_1['Data']))
		file_with_backup.write(base64.b64decode(json_2['Data']))
		file_with_backup.write(base64.b64decode(json_backup1['Data']))
		file_with_backup.write(base64.b64decode(json_backup2['Data']))
		file_with_backup.close()

	#shard 1 is dead
	elif Connected2 == 1 and Connected3 == 1:
		#download primary bytes from shard 2 and shard 3
		for buffer in rec_shard(sock1):
			file_data2 = buffer
			json_2 = json.loads(file_data2)
		for buffer in rec_shard(sock2):
			file_data3 = buffer
			json_3 = json.loads(file_data3)
		#download backup bytes from shard 2
		msg_send2 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json2['BytesFrom1'], 'BytesTo': json2['BytesTo1']}
		backup_req2 = json.dumps(msg_send2)
		print backup_req2
		while backup_req2:
			bytes = sock1.send(backup_req2)
			backup_req2 = backup_req2[bytes:]
		backup_data2 = ''
		for buffer in rec_shard(sock2):
			backup_data2 = buffer
		json_backup2 = json.loads(backup_data2)
		#download backup bytes from shard 3
		msg_send3 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json3['BytesFrom1'], 'BytesTo': json3['BytesTo1']}
		backup_req3 = json.dumps(msg_send3)
		while backup_req3:
			bytes = sock2.send(backup_req3)
			backup_req3 = backup_req3[bytes:]
		backup_data3 = ''
		for buffer in rec_shard(sock2):
			backup_data3 = buffer
		json_backup3 = json.loads(backup_data3)
		#assemble data, write to file in correct order
		file_with_backup = open(json_2['Filename'],'w+')
		file_with_backup.write(base64.b64decode(json_2['Data']))
		file_with_backup.write(base64.b64decode(json_3['Data']))
		file_with_backup.write(base64.b64decode(json_backup2['Data']))
		file_with_backup.write(base64.b64decode(json_backup3['Data']))
		file_with_backup.close()
	
	#shard 2 is dead
	elif Connected1 == 1 and Connected3 == 1:
		#download primary bytes from shard 1 and shard 3
		for buffer in rec_shard(sock):
			file_data1 = buffer
			json_1 = json.loads(file_data1)
		for buffer in rec_shard(sock2):
			file_data3 = buffer
			json_3 = json.loads(file_data3)
		#download backup bytes from shard 1
		msg_send1 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json1['BytesFrom2'], 'BytesTo': json1['BytesTo2']}
		backup_req1 = json.dumps(msg_send1)
		print backup_req1
		while backup_req1:
			bytes = sock.send(backup_req1)
			backup_req1 = backup_req1[bytes:]
		backup_data1 = ''
		for buffer in rec_shard(sock1):
			backup_data1 = buffer
		json_backup1 = json.loads(backup_data1)
		#download backup bytes from shard 3
		msg_send3 = {'MessageType': 'REQUESTDATA', 'Filename': str(File), 'BytesFrom': json3['BytesFrom2'], 'BytesTo': json3['BytesTo2']}
		backup_req3 = json.dumps(msg_send3)
		while backup_req3:
			bytes = sock2.send(backup_req3)
			backup_req3 = backup_req3[bytes:]
		backup_data3 = ''
		for buffer in rec_shard(sock2):
			backup_data3 = buffer
		json_backup3 = json.loads(backup_data3)
		#assemble data, write to file in correct order
		file_with_backup = open(json_3['Filename'],'w+')
		file_with_backup.write(base64.b64decode(json_1['Data']))
		file_with_backup.write(base64.b64decode(json_3['Data']))
		file_with_backup.write(base64.b64decode(json_backup1['Data']))
		file_with_backup.write(base64.b64decode(json_backup3['Data']))
		file_with_backup.close()


else:

	total_bytes = {'MessageType': 'BYTESTORED'}
	encoded_msg = json.dumps(total_bytes)
	print encoded_msg
	print 'asking for currently used storage'
	while encoded_msg:
		bytes = sock.send(encoded_msg)
		bytes = sock1.send(encoded_msg)
		bytes = sock2.send(encoded_msg)
		encoded_msg = encoded_msg[bytes:]

	rec_bytes1 = ''
	rec_bytes2 = ''
	rec_bytes3 = ''
	for buffer in rec_shard(sock):
		rec_bytes1 = buffer
	for buffer in rec_shard(sock1):
		rec_bytes2 = buffer
	for buffer in rec_shard(sock2):
		rec_bytes3 = buffer
		
	json_obj1 = json.loads(rec_bytes1)
	print 'reply was ' + json_obj1['BytesStored'] + 'bytes'
	json_obj2 = json.loads(rec_bytes2)
	print 'reply was ' + json_obj2['BytesStored'] + 'bytes'
	json_obj3 = json.loads(rec_bytes3)
	print 'reply was ' + json_obj3['BytesStored'] + 'bytes'
	
	f1 = open(File,'r+')
	upload_size= file_size(File)

	total = int(json_obj1['BytesStored']) + int(json_obj2['BytesStored']) + int(json_obj3['BytesStored']) + int(upload_size)
	total = total/3

	#upload to each shard
	to_shard1 = balance_load(total,int(json_obj1['BytesStored']))
	to_shard2 = balance_load(total,int(json_obj2['BytesStored']))
	to_shard3 = balance_load(total,int(json_obj3['BytesStored']))
	balance = upload_size%3
	to_shard1+=balance

	#print 'upload sizes are'
	#print 'shard1'
	#print file_size(File)

	send_file1 = {'MessageType': 'DATA', 'Filename': str(File), 'BytesFrom': '0', 'BytesTo': str(to_shard1-1), 'Data': base64.b64encode(str(f1.read(to_shard1)))}
	send_file2 = {'MessageType': 'DATA', 'Filename': str(File), 'BytesFrom': str(to_shard1), 'BytesTo': str(to_shard1+to_shard2-1), 'Data': base64.b64encode(str(f1.read(to_shard2)))}
	send_file3 = {'MessageType': 'DATA', 'Filename': str(File), 'BytesFrom': str(to_shard1+to_shard2), 'BytesTo': str(to_shard1+to_shard2+to_shard3-1), 'Data': base64.b64encode(str(f1.read(to_shard3)))}
	
	encoded_msg1= json.dumps(send_file1)
	encoded_msg2= json.dumps(send_file2)
	encoded_msg3= json.dumps(send_file3)
	#print 'uploading to shard1'
	#print file_size(File)
	#print 'to shard1'
	while encoded_msg1:
		bytes = sock.send(encoded_msg1)
		encoded_msg1 = encoded_msg1[bytes:]
	while encoded_msg2:
		bytes = sock1.send(encoded_msg2)
		encoded_msg2 = encoded_msg2[bytes:]
	while encoded_msg3:
		bytes = sock2.send(encoded_msg3)
		encoded_msg3 = encoded_msg3[bytes:]
	# Receive the data in small chunks and retransmit it
	for buffer in rec_shard(sock):
		upload_status1 = buffer
	for buffer in rec_shard(sock1):
		upload_status2 = buffer
	for buffer in rec_shard(sock2):
		upload_status3 = buffer

	
	json_obj1 = json.loads(upload_status1)
	print json_obj1['Content']
	json_obj2 = json.loads(upload_status2)
	print json_obj2['Content']
	json_obj3 = json.loads(upload_status3)
	print json_obj3['Content']
