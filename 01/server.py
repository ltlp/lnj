#
#LnJ server 
#


import zmq
import time
import sys
import sqlite3
import hashlib



# port = ""

# if len(sys.argv) > 1:
#         port = sys.argv[1]
#         int(port)


#REP/REQ arch for sending messages. PUB/SUB for distributing clients 
zmq_context = zmq.Context()

socket_server = zmq_context.socket(zmq.REP)
socket_pub = zmq_context.socket(zmq.PUB)

socket_pub.bind("tcp://*:55010") 
socket_server.bind("tcp://*:55011") 

poller = zmq.Poller()
poller.register(socket_server, zmq.POLLIN)\


# SQL
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# sha224
sql_command = """
CREATE TABLE users (
username VARCHAR(30) PRIMARY KEY,
password VARCHAR(50),
timestampp TIMESTAMP 
); """

try:
	cursor.execute(sql_command)
except:
	pass

connection.commit()
#connection.close()


authenticated_users = {}

users = cursor.execute("SELECT * FROM users")
for user in users:
	authenticated_users[user[0]] = user[1]

print authenticated_users


while True: 

	msg_events = dict(poller.poll(1000)) #time in milliseconds until time out
	
	if msg_events.get(socket_server) == zmq.POLLIN:

		data = socket_server.recv_json() 
		print data

		# if data['authentication'] == True: 

		# 	if data['user'] in authenticated_users:

		# 		hashed_password = data['password']

		# 		print hashlib.sha224(data['password']).hexdigest() 
		# 		print authenticated_users[data['user']]

		# 		if hashlib.sha224(data['password']).hexdigest() == authenticated_users[data['user']]:

		# 			print 'success'

		# 		else:

		# 			print 'password invalid'

		# 	else:
		# 		 print 'user not in database'

		# else:

		# 	print "not authentication packet"




		socket_server.send(b'\x00') 

		socket_pub.send_json(data) 