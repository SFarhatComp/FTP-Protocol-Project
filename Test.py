import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
# binding the socket to the local host. With socket we send and receive data, 
s.listen(5) # prepared to listen to everything

while True:

    clientsocket,address =s.accept()  #When a connection is received, store the value in client socket and store their source address in address
    print(f"Connection from {address} has been established ! ")
    clientsocket.send(bytes("Welcome to the server!","utf-8"))