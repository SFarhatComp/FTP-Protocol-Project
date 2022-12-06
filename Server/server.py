import socket


endString = b"<40097236>"


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostname(),9999))
# binding the socket to the local host. With socket we send and receive data, 
server.listen() # prepared to listen to everything



#Responding to make sure the connection is established

#***********************Backend of the project*************************

#Receiving file from client: 

while True:


    serversocket,address =server.accept()  #When a connection is received, store the value in client socket and store their source address in address
    print(f"Connection from {address} has been established ! ")
    serversocket.send(bytes("Welcome to the server!","utf-8"))
    
    while True:
    
        Request=serversocket.recv(8).decode()
        Op_code = Request[0:3]

        print(f"The current opcode is {Op_code}")
        if Op_code =="":
            break

        if Op_code=="011":
            print(f"Help from {address} has been asked ! ")
            
            serversocket.send(bytes("The accepted requests are : Help, Put, Get, Change, Bye","utf-8"))
            
            print("")
            
            #serversocket.close()
            #exit(0)
            
        
        elif Op_code=="000":

            File_Name_Length=Request[3:]
            print(f"The file name length is : {File_Name_Length}")
            File_Name_Length_decimal=(int(File_Name_Length,2)+4)
            print(f"The file name length in deicmal is : {File_Name_Length_decimal}")

            file_name=serversocket.recv(File_Name_Length_decimal).decode("utf-8")
            print(f"The file : {file_name} has been received properly")
            #We need a byte string in order to store the values of the file sent, we will continously update the file 
        
            file_bytes=b""
            #Setting a flag for end of transfer: 
            Finished=False
            file=open(file_name,"wb") ## Open a file with the name of the file passed , and then we will write into it any data bytes that we need 

            while not Finished:
                data_received=serversocket.recv(1024)
                #print(f"The Current Data received is {data_received}")
                #print(f"The current value of  File Byte is : {file_bytes}")
                file_bytes+=data_received
                if file_bytes[-10:] == b"<40097236>":
                    Finished = True
                    print("The File has been properly uploaded")
                

            file.write(file_bytes[0:-10])
            file.close()
            print("The transfer of the file is finished")    #When done writing into it, close the file
        
        elif Op_code =="001":
            File_Name_Length=Request[3:]
            print(f"The file name length is : {File_Name_Length}")
            File_Name_Length_decimal=(int(File_Name_Length,2))
            print(f"The file name length in deicmal is : {File_Name_Length_decimal}")
            file_name=serversocket.recv(File_Name_Length_decimal-1).decode("utf-8")
        
            with open(file_name,'rb') as file : 
                data=file.read()
            
            serversocket.send(data)
            serversocket.send(endString)
            print(f"The file has been succesfully fetched and sent back to {address}")

        
        elif Op_code == "010":
            File_Name_Length=Request[3:8]
            print(f"The file length of the file to change is : {File_Name_Length}")
            File_Name_Length_decimal=(int(File_Name_Length,2))
            print(File_Name_Length_decimal)


            oldName=serversocket.recv(File_Name_Length_decimal-1).decode("utf-8")
            print(f"the old file name is : {oldName}")
            NewNameLength=serversocket.recv(8).decode()
            print(f"The File length of the new Name is : { NewNameLength}")
            NewName=serversocket.recv(int(NewNameLength,2)-1).decode("utf-8")

            print(f"The file is to be changed from {oldName} to {NewName} ")
            

            






