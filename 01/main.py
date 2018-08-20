from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle
import zmq
import sys
from threading import Thread


class LnJ(Widget):

    def __init__(self, **kwargs):

        super(LnJ, self).__init__(**kwargs)

        print Window.height
        print Window.width


        layout = AnchorLayout(anchor_x='left', anchor_y='top', width=Window.width, height=Window.height*.15)
        self.text_layout = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y= None, pos = (0, Window.height*.1), width=Window.width, height=Window.height)


        self.scroller = ScrollView( scroll_distance=50, pos=(0, Window.height*.15 ), size=(Window.width, Window.height*.85))

        with self.scroller.canvas.after:
            Color(1,1,1,.5)
            Rectangle(pos=self.scroller.pos, size=self.scroller.size)



        self.chat_container = FloatLayout(pos=(0, Window.height*.15),pos_hint=(None,None), height=Window.height*2)

        self.chat_label = Label(text='', valign='bottom', halign='left', padding=(20,10),  pos=(0,0))

        # with self.chat_label.canvas.after:
        #     Color(1,1,1,.1)
        #     Rectangle(pos=self.chat_label.pos, size=self.chat_label.size)
        #boxlayout_chat = BoxLayout(orientation='horizontal')
        #boxlayout_chat.add_widget(self.chat_label)
        self.scroller.add_widget(self.chat_container)
        self.chat_container.add_widget(self.chat_label)
        
        #self.text_layout.add_widget(self.chat_label)


        boxlayout = BoxLayout(orientation='horizontal')

        boxlayout_2 = BoxLayout(orientation='horizontal')
        boxlayout_master = BoxLayout(orientation='vertical')
        #self.text_box_display = BoxLayout(orientation='vertical')





        btn1 = Button(text='Connect', width=200, on_press=self.connect)
        btn2 = Button(text='Send', on_press=self.send)

        self.textinput = TextInput(on_text_validate=self.send, multiline=False)

        boxlayout.add_widget(btn1)
        boxlayout.add_widget(btn2)
        boxlayout_2.add_widget(self.textinput)
        boxlayout_master.add_widget(boxlayout_2)
        boxlayout_master.add_widget(boxlayout)
        



        btn = Button(text='Connect')

        #layout.add_widget(boxlayout_chat)
        layout.add_widget(boxlayout_master)
        #layout.add_widget(boxlayout_2)
        #layout.add_widget(boxlayout_2)

        #text_layout.add_widget(self.text_box_display)


        self.connect('string')
        Clock.schedule_interval(self.query_server, .2)
        #Clock.schedule_interval(self.thread_Join, 1)



        self.add_widget(layout)
        self.add_widget(self.scroller)
        


    def thread_join(self, clock):
        self.listen_thread.join()


    def esc_markup(self, msg):
        return (msg.replace('&', '&amp;')
            .replace('[', '&bl;')
            .replace(']', '&br;'))



    def query_server(self, clock):

        # while True:

        #     events = dict(self.poller.poll(3000))
        #     if events.get(self.chat_sock) == zmq.POLLIN:
        #         message = self.client_socket.recv()


                msg_events = dict(self.poller.poll(50))
                print msg_events
                if self.sub_socket in msg_events:



               # try:
                    print "query server"
                    data = self.sub_socket.recv_json()
                    user, message = data['user'], data['message']
                    print user
                    #code, message = message.split()
                    print user, message
                    self.chat_label.text += ('\t{}: {}\n'.format(user, message))
                    #self.chat_label.text += ('\t[b][color=2980b9]{}:[/color][/b] {}\n'.format(user, self.esc_markup(message)))
                    #self.text_layout.add_widget(Label(text=message, halign='left', valign='top', height=25, width=Window.width))

                # except:
                #     pass

    def send(self, button=None):

            data = {
            'user':"anon",
            'message':str(self.textinput.text)
            }
            self.client_socket.send_json(data)
            message_from_server = self.client_socket.recv()
            print "message circuit complete"
            self.textinput.text = ''


        #print self.textinput.text


    def connect(self, button):

        port = "55010"
        # if len(sys.argv) > 1:
        #   port = sys.argv[1]
        #   int(port)

        # if len(sys.argv) > 2:
        #   port1 = sys.argv[2]
        #   int(port1)

        self.context = zmq.Context()
        print "Connecting to server..."


        self.poller = zmq.Poller()



        self.client_socket = self.context.socket(zmq.REQ)
        self.sub_socket = self.context.socket(zmq.SUB)

        #self.socket.connect ("tcp://45.33.59.7:%s" % port)
        self.sub_socket.connect ("tcp://127.0.0.1:%s" % port)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')

        #self.client_socket.connect("tcp://45.33.59.7:55011")
        self.client_socket.connect("tcp://127.0.0.1:55011")


        self.poller.register(self.client_socket, zmq.POLLIN)
        self.poller.register(self.sub_socket, zmq.POLLIN)

        #print "Sending request ", request,"..."
        data = {
            'user': "anon",
            'message': "test data",
        }

        self.client_socket.send_json(data)
        message = self.client_socket.recv()

        print "connected and paired"
        #print "Received reply ", request, "[", message, "]"

        #self.listen_thread = Thread(target=self.query_server, args=())
        #self.listen_thread.start()




if __name__ == "__main__":
    LnJ().run()








