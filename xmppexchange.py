import logging
import threading
import configparser

import chatexchange.client
import chatexchange.events

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from bs4 import BeautifulSoup

global config
config = configparser.ConfigParser()
config.read('xmppexchange.ini')

class XMPPExchange(ClientXMPP):

    global relay
    relay = False

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.on_xmpp_message)
        self.add_event_handler("changed_status", self.wait_for_presences)
        self.received = set()
        self.presences_received = threading.Event()

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.presences_received.wait(5)
        print ("Logged in to XMPP as "+self.boundjid.bare)

        host_id = config['stackexchange']['host']
        room_id = config['stackexchange']['room']
        email = config['stackexchange']['email']
        password = config['stackexchange']['password']

        client = chatexchange.client.Client(host_id)
        client.login(email, password)
        global me
        me = client.get_me()
        print ("Logged in to StackExchange as "+me.name)

        global room
        room = client.get_room(room_id)
        room.join()
        room.watch(self.on_stack_message)

    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if (config['xmppexchange']['allowedjid'] == pres['from'].bare):
            self.relay = (pres.get_type() == "available")
            print("Relay status is now on: " + str(self.relay))
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    def on_stack_message(self, message, client):
        if not isinstance(message, chatexchange.events.MessagePosted):
            return
        if ((self.relay == True) and (message.user is not me)) or (str("@"+me.name).lower() in message.content.lower()):
            soup = BeautifulSoup(message.content, "html.parser")
            message_content = message.user.name + ": " + soup.get_text()
            self.send_message(mto=config['xmppexchange']['allowedjid'], mbody=message_content, mtype='chat')

    def on_xmpp_message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("Received message from " + msg['from'].bare + " with content " + msg['body'])
            if (config['xmppexchange']['allowedjid'] == msg['from'].bare):
                room.send_message(msg['body'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')

    xmpp = XMPPExchange(config['xmpp']['jid'], config['xmpp']['password'])
    xmpp.connect()
    xmpp.process(block=True)