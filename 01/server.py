import zmq
import time
import sys

# port = "55010"

# if len(sys.argv) > 1:
#         port = sys.argv[1]
#         int(port)

zmq_context = zmq.Context()
#publish_context = zmq.Context()

socket_server = zmq_context.socket(zmq.REP)
socket_pub = zmq_context.socket(zmq.PUB)

socket_pub.bind("tcp://*:55010") 
socket_server.bind("tcp://*:55011") 

poller = zmq.Poller()
poller.register(socket_server, zmq.POLLIN)\


#socket.bind("tcp://*:%s" % port) 
 
while True: 
		#classic client/server arch

				msg_events = dict(poller.poll(1000))
				if msg_events.get(socket_server) == zmq.POLLIN:
					print "got a message for a chat client!"
					data = socket_server.recv_json() 
					user = data['user']
					message = data['message']


					socket_server.send(b'\x00') 
					print "Received request: ", message 
	 
			 
					#time.sleep (1) 
			 
					#new pub/sub arch  
					if message == "Hello": 
							pass 
					else: 
							print "Publishing to clients"
							print data
							socket_pub.send_json(data) 

				print "Loopin"