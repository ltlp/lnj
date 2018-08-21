#
#LnJ server 
#


import zmq
import time
import sys



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


 
while True: 
	
	msg_events = dict(poller.poll(1000)) #time in milliseconds until time out

	if msg_events.get(socket_server) == zmq.POLLIN:

		data = socket_server.recv_json() 
		socket_server.send(b'\x00') 
		socket_pub.send_json(data)