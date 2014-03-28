#!/usr/bin/env python


"""
TCP file server using Twisted.  The goal of this simple demo was to show:
a) How a JSON string can be used to send complex data (lists, dictionaries)
b) How this could be used to send commands and data to go with those commands
c) how the server could be made recognize commands and be structured to handle them.

(NOTE: This is just a demo.  It's not necessarily a great design. It's to show how
something might be done.)

3rd party libraries need to be installed to run this!  Use pip to install:
a) Twisted

How to run these.  (Might be easier to run these from the command-line.)
a) Start the server, this program.
b) Start the client, file1_client_tw.py, on the same computer. (In a different window.)
c) In the client, type a Python dictionary, where one key is "cmd" -- this could be
the "command" you're sending.  The server recognizes these commands: user, write, delete.
A method is called for each one of these, and right now the server just sends
back an acknowledgment and ignores other data in the dictionary.  But you can see how this
could be the start of implementing a protocol.
Example of valid input:  {"cmd" : "user", "user_id" : "horton"}
d) Hit return in the client to stop the client.
e) In the server window, Hit CTRL-C or whatever your operating system requires to kill a running program.

It should be possible to run these on two different computers.
Start the server on one machine.
When you start the client on the 2nd machine, give a command-line argument: the IP address
or full internet hostname of the server machine.

"""

from twisted.internet import protocol, reactor
from time import ctime, time
import os
import json

PORT = 21567

allowed_users = ["tom", "ali"]


class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print '...connected from:', clnt

    def dataReceived(self, in_msg):
        self.process_incoming(in_msg)
        # out_msg = '[%s] %s' % (ctime(), in_msg)
        # self.transport.write(out_msg)


    def handle_user_cmd(self, msg_data):
        self.transport.write("response for 'user' cmd")

    def handle_write_cmd(self, msg_data):
        self.transport.write("response for 'write' cmd")

    def handle_delete_cmd(self, msg_data):
        self.transport.write("response for 'delete' cmd")

    def handle_invalid_cmd(self, msg_data):
        self.transport.write("response for 'invalid' cmd")


    def process_incoming(self, json_msg):
        try:
            msg_data = json.loads(json_msg)
            cmd = msg_data["cmd"]
        except ValueError:
            cmd = None
        print "Server processing: ", cmd

        if cmd == "user":
            self.handle_user_cmd(msg_data)
        elif cmd == "write":
            self.handle_write_cmd(msg_data)
        elif cmd == "delete":
            self.handle_delete_cmd(msg_data)
        else:
            self.handle_invalid_cmd(json_msg)


    def test_process_incoming1(self):
        self.process_incoming('{"cmd" : "user", "user_id" : "horton"}')


def store_data(user, filename, data):
    path = os.path.join(os.getcwd(), user)
    if not os.path.exists(path):
        os.mkdir(path)
    with open( os.path.join(path, filename), "w") as f:
        f.write(data)
    print "server wrote data to: ", os.path.join(path, filename)


# def test_store_data1():
#     store_data("user1", "foo.txt", "here's some data stored at "+ str(time()))

if __name__ == "__main__":
    # test_process_incoming1()
    factory = protocol.Factory()
    factory.protocol = TSServProtocol
    print 'waiting for connection on PORT: ', PORT
    reactor.listenTCP(PORT, factory)
    reactor.run()