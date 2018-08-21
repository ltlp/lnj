
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

        self.height = Window.height
        self.width = Window.width

        self.user = ''


        self.layout = AnchorLayout(anchor_x='left', anchor_y='top', width=Window.width, height=Window.height*.15)
        self.text_layout = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y= None, pos = (0, Window.height*.1), width=Window.width, height=Window.height)
        self.chat_container = FloatLayout(pos=(0, Window.height*.15),pos_hint=(None,None), height=Window.height*2)
        self.boxlayout = BoxLayout(orientation='horizontal')
        self.boxlayout_2 = BoxLayout(orientation='horizontal')
        self.boxlayout_master = BoxLayout(orientation='vertical')
        self.chat_label = Label(text='', valign='bottom', halign='left', padding=(20,10),  pos=(0,0))
        self.textinput = TextInput(on_text_validate=self.send, multiline=False)
        self.scroller = ScrollView( scroll_distance=50, pos=(0, Window.height*.15 ), size=(Window.width, Window.height*.85))
        self.btn1 = Button(text='Connect', width=200, on_press=self.connect)
        self.btn2 = Button(text='Send', on_press=self.send)
        self.btn = Button(text='Connect')

        self.scroller.add_widget(self.chat_container)
        self.chat_container.add_widget(self.chat_label)
        self.boxlayout.add_widget(btn1)
        self.boxlayout.add_widget(btn2)
        self.boxlayout_2.add_widget(self.textinput)
        self.boxlayout_master.add_widget(boxlayout_2)
        self.boxlayout_master.add_widget(boxlayout)
    

        self.layout.add_widget(boxlayout_master)
        self.add_widget(layout)
        self.add_widget(self.scroller)


        self.connect('string')
        Clock.schedule_interval(self.query_server, .2)

        with self.scroller.canvas.after:
            Color(1,1,1,.5)
            Rectangle(pos=self.scroller.pos, size=self.scroller.size)

        

    def query_server(self, clock):

        msg_events = dict(self.poller.poll(50))
        if self.sub_socket in msg_events:

            data = self.sub_socket.recv_json()
            user, message = data['user'], data['message']
            self.chat_label.text += ('\t{}: {}\n'.format(user, message))


    def send(self, button=None):

            data = {
            'user': self.user,
            'message':str(self.textinput.text)
            }

            self.client_socket.send_json(data)
            message_from_server = self.client_socket.recv()
            self.textinput.text = ''



    def connect(self, button):

        port = "55010"

        self.context = zmq.Context()
        self.poller = zmq.Poller()

        self.client_socket = self.context.socket(zmq.REQ)
        self.sub_socket = self.context.socket(zmq.SUB)

        self.sub_socket.connect ("tcp://127.0.0.1:%s" % port)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')

        self.client_socket.connect("tcp://127.0.0.1:55011")


        self.poller.register(self.client_socket, zmq.POLLIN)
        self.poller.register(self.sub_socket, zmq.POLLIN)

        data = {
            'user': "anon",
            'message': "test data",
        }

        self.client_socket.send_json(data)
        message = self.client_socket.recv()



if __name__ == "__main__":
    LnJ().run()








