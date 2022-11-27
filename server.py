import socket


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostname(),9999))
# binding the socket to the local host. With socket we send and receive data, 
server.listen() # prepared to listen to everything

serversocket,address =server.accept()  #When a connection is received, store the value in client socket and store their source address in address
print(f"Connection from {address} has been established ! ")
serversocket.send(bytes("Welcome to the server!","utf-8"))
#Responding to make sure the connection is established





#***********************Backend of the project*************************

#Receiving file from client: 


Request=serversocket.recv(8).decode()
print(Request)

Op_code = Request[0:3]
print(f"The Op_Code is : {Op_code}")
File_Name_Length=Request[3:]
print(f"The file name length is : {File_Name_Length}")
File_Name_Length_decimal=(int(File_Name_Length,2)+4)
print(f"The file name length in deicmal is : {File_Name_Length_decimal}")


if Op_code=="011":
    print(f"Connection from {address} has been closed ! ")
    serversocket.close()


elif Op_code=="000":
    file_name=serversocket.recv(File_Name_Length_decimal).decode("utf-8")
    print(f"The file : {file_name} has been received properly")
    #We need a byte string in order to store the values of the file sent, we will continously update the file 
   
    file_bytes=b""
    #Setting a flag for end of transfer: 
    Finished=False
    file=open(file_name,"wb") ## Open a file with the name of the file passed , and then we will write into it any data bytes that we need 

    while not Finished:
        data_received=serversocket.recv(1024)
        print(f"The Current Data received is {data_received}")
        print(f"The current value of  File Byte is : {file_bytes}")
        if file_bytes[-10:] == b"<40097236>":
            Finished = True
            print("The File has been properly uploaded")
        else:
            file_bytes+=data_received

    file.write(file_bytes[0:-10])
    file.close()
    print("The transfer of the file is finished")    #When done writing into it, close the file


else:
    print("------------------------------------------------------------------")
server.close()


