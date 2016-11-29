#!/bin/python

from socket import *
import sys

def chat(connection_socket, clientname, username):
    """Chat

    Initiates a chart session with the client
    Lets them send the first messages
    """
    to_send = ""
    while 1:
        # continue chat until we break
        # get all of the characters from the user
        received = connection_socket.recv(501)[0:-1]
        # if we received nothing, print connection closed and close connection
        if received == "":
            print "Connection closed"
            print "Waiting for new connection"
            break
        # print the clients name with their message
        print "{}> {}".format(clientname, received)
        # grab input on our side to send to user
        to_send = ""
        while len(to_send) == 0 or len(to_send) > 500:
            to_send = raw_input("{}> ".format(username))
            # send it to the client if the message is not \quit
        if to_send == "\quit":
            print "Connection closed"
            print "Waiting for new connection"
            break
        connection_socket.send(to_send)

def handshake(connection_socket, username):
    """handshake
    
    This function exchanges usernames with the incoming connection
    """
    # get the client's name
    clientname = connection_socket.recv(1024)
    # send our username to the client
    connection_socket.send(username)
    return clientname

if __name__ == "__main__":
    # If the number of arguments is wrong, exit
    if len(sys.argv) != 2:
        print "You must specify the port number for the server to run"
        exit(1)
    # get the port number from the user and create a TCP socket
    serverport = sys.argv[1]
    serversocket = socket(AF_INET, SOCK_STREAM)
    # bind the socket to the port specified by the user
    serversocket.bind(('', int(serverport)))
    # listen on the port for incoming messages
    serversocket.listen(1)
    # ask the user for their name, must be less than 11 characters
    username = ""
    while len(username) == 0 or len(username) > 10:
        username = raw_input("Please enter a user name of 10 characters or less: ")
        print "The server is ready to receive incoming messages"
    while 1:
        # keep doing this until signal interup
        # create a new socket if there is an incoming connection
        connection_socket, address = serversocket.accept()
        # print that we have received a connection
        print "received connection on address {}".format(address)
        # chat with the incoming connection, handshake with them first
        chat(connection_socket, handshake(connection_socket, username), username)
        # close the connection when we are done chatting
        connection_socket.close()

