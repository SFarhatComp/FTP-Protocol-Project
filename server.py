import socket



server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostname(),9999))
# binding the socket to the local host. With socket we send and receive data, 
server.listen() # prepared to listen to everything

serversocket,address =server.accept()  #When a connection is received, store the value in client socket and store their source address in address
print(f"Connection from {address} has been established ! ")
serversocket.send(bytes("Welcome to the server!","utf-8"))
#Responding to make sure the connection is established





#***********************BackEND of the project*************************

#Receiving file from client: 


Request=serversocket.recv(8).decode()

print(Request)



if Request.upper()=="BYE":
    print(f"Connection from {address} has been closed ! ")
    serversocket.close()
   

else:
    file_name=serversocket.recv(16).decode("utf-8")
    print(f"The file : {file_name} has been received properly")
    #We need a byte string in order to store the values of the file sent, we will continously update the file 
    #Setting a flag for end of transfer: 

    file=open(file_name,"wb") ## Open a file with the name of the file passed , and then we will write into it any data bytes that we need 

    Finished=False
    while not Finished:
        data_received=serversocket.recv(1024)
        if file_bytes[-10:] == b"<40097236>":
            Finished = True
            print("The File has been properly uploaded")
        else:
            file_bytes+=data_received


    file.write(file_bytes[0:-10])
    file.close()    #When done writing into it, close the file



server.close()


