import socket
import sys
import json
import os
import datetime

serverPort = 42069


def getUserFromDB(identifier, password):
    #check if user exists
    #check if password matches
    #get user info or just id
    return #user or true

def server():

    pid = 0

	#Create server socket that uses IPv4 and TCP protocols 
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("could not create socket")
        sys.exit(1)
	
	#Associate 13000 port number to the server socket
    try:
        serverSocket.bind(('', serverPort))
    except socket.error as e:
        print("could not bind socket")
        sys.exit(1)        
		
	#The server can have up to 5 connection in its queue waiting for acceptance
    print("The server is ready to accept connections")
    serverSocket.listen(5)
    while 1:
        try:
			#Server accepts client connection
            connectionSocket, addr = serverSocket.accept()
			
			#fork here to create child process (client)
            pid = os.fork()
			
			#if statement to see if it has actually forked
			#if it has sends welcome message to client
            if pid == 0:
                serverSocket.close()
                client = user_verification(connectionSocket) 
                if not client:
                    connectionSocket.close()
                    clientpid = os.getpid()
                    os.kill(clientpid,9)

                print ("Connection Accepted and Symmetric Key Generated for client: " + client)
				
                connectionSocket.send(client.encode('ascii')) #TODO encrypt
				
					
					
            connectionSocket.close()                     
						
        except socket.error as e:
            print('An error occured:',e)
            serverSocket.close() 
            sys.exit(1)  



def user_verification(socket):
    with open('temporary_user_pass.json', 'r') as json_file: #change this to use database
        user_data = json.load(json_file)
	
	#Get username
    user_name = socket.recv(2048) #receive username input
    user_name = user_name.decode('ascii')

	#Get password
    password = socket.recv(2048) #receive password input
    password = password.decode('ascii')

	#check user and pw info
    if user_name in user_data.keys() and password == user_data[user_name]:
        return user_name #return username if valid

    msg = 'Invalid username or password'
    socket.send(msg.encode('ascii'))
    print ("The received client information: " + user_name + 
			" is invalid (ConnectionTerminated).")
    return 
