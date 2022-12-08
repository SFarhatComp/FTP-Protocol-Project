import socket
import os
import os.path 


endString = b"<40097236>" # End string that we add to file to make sure that we ahve reached trhe end


#----------------binding the socket to the local host. With socket we send and receive data----------------------------- 

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostname(),9999))

print(f"The Server is currently being hosted on IP: {socket.gethostbyname(socket.gethostname())}, with the port 9999")
server.listen() # prepared to listen to everything


#Responding to make sure the connection is established

#***********************Backend of the project*************************

#Receiving file from client: 

while True: 

    #First while true allow an infinite loop of the server, making it always listen to new connections


    serversocket,address =server.accept()  #When a connection is received, store the value in client socket and store their source address in address
    print(f"Connection from {address} has been established ! ")
    serversocket.send(bytes("Welcome to the server!","utf-8"))
    Debug = input('Do you wish to be in debug mode (1 -> yes / 0-> no)')

    
    while True:
    
        #Once the client is connected, then we parse what ever values we get from the client and compute what we need to compute 
        
        Request=serversocket.recv(8).decode()  # This first receive will always containt the opcode that we need stored as the 3 bit from whatever command is sent. We always send 8 bits from the client side and recv 8 bit
        Op_code = Request[0:3] #first 3 char will always represent the Opcode

        
            
        if Op_code =="": #If ever we receive nothing as an opcode, it means we have asked for a close from the server side 
            if Debug == 1:
                print(f'Nothing was received, nothing was sent \n Closing connection with {address}')
            break


        if Op_code=="011":  # if we receive this opcode it asks for help
            print(f"Help from {address} has been asked ! ")
            
            Help_data = "Help, Put, Get, Change, Bye"
            Help_data_Length = bin(len(Help_data)+1)[2:]
            
        

            while len(Help_data_Length)<5:
                Help_data_Length = "0"+Help_data_Length
            

            serversocket.send(("110"+Help_data_Length).encode())
            serversocket.send(Help_data.encode())

            if Debug == 1:
                print(f'The received request is {Op_code}')
                print(f'This is what is sent and outputted to the user : ' + Help_data)
                print(f'The message sent is 110 ' + Help_data_Length)
            

        elif Op_code=="000":
                            #if we receive this op  code we need to put the file transmitted
            File_Name_Length=Request[3:]
            File_Name_Length_decimal=(int(File_Name_Length,2)-1)
            print(f"The file name length in deicmal is : {File_Name_Length_decimal}")

            #We get the file name lenght so we know how much bytes to receive from the client. 

            file_name=serversocket.recv(File_Name_Length_decimal).decode("utf-8")
            print(f"The file : {file_name} has been received properly")
            
            #We need a byte string in order to store the values of the file sent, we will continously update the file 
            file_bytes=b""
            #Setting a flag for end of transfer: 
            Finished=False
            file=open(file_name,"wb") ## Open a file with the name of the file passed , and then we will write into it any data bytes that we need 
            while not Finished:
                data_received=serversocket.recv(1024)
                file_bytes+=data_received
                if file_bytes[-10:] == b"<40097236>":
                    Finished = True
                    print("The File has been properly uploaded")
                     # This implementation means that we have a while loop that will constantly append to the file_byte which is a byte string. We are constantly adding bytes values to it , that we get from the stream of packages sent by the server using the send all/receive(1024)
            #Then we always verify if the last 10 digits are the same as the end of file cusotm flag that we have sent. When they are equal it means that we have reached the end of the file, exiting the loop, and setting it as finished the transfer. 
            #We then write to the open file .

            file.write(file_bytes[0:-10])
            file.close()

            print("The transfer of the file is finished")    #When done writing into it, close the file
        
            serversocket.send(("00000000").encode())

            if Debug == 1:
                print(f'The received request is {Op_code}')
                print(f'The name of the file received is {file_name}')
                print(f'The file name lenght received is {File_Name_Length}')
                print(f'The message sent is 00000000')




        elif Op_code =="001": # with this opcode we are requesting a get. Meaning we parse the name and data and send it to the client
            File_Name_Length=Request[3:]
            File_Name_Length_decimal=(int(File_Name_Length,2))
            print(f"The file name length in deicmal is : {File_Name_Length_decimal}")
            file_name=serversocket.recv(File_Name_Length_decimal-1).decode("utf-8")
        
            
    
            if os.path.isfile(file_name):


                with open(file_name,'rb') as file : 
                    data=file.read()


                serversocket.send(("001"+File_Name_Length).encode()) #Sending back the correct response message with the file name length
                serversocket.send(file_name.encode())#Sending the file name            
                serversocket.sendall(data)
                serversocket.sendall(endString)

                #Sending the data and the endstring in order to make sure it has been properly received
                print(f"The file has been succesfully fetched and sent back to {address}")
                if Debug == 1:
                    print(f'The received request is {Op_code}')
                    print(f'The name of the file received is {file_name}')
                    print(f'The final name lenght received is {File_Name_Length}')
                    print(f'The message sent is 001')


            else:
            
                serversocket.send(("01000000").encode())
                print("The client has asked for a file that does not exist")
                if Debug == 1:
                    print(f'The received request is {Op_code}')
                    print(f'The name of the file received is {file_name}')
                    print(f'The file name lenght received is {File_Name_Length}')
                    print(f'The message sent is 01000000')

                





        
        elif Op_code == "010": #With this opcode we are requesting a change of name
            File_Name_Length=Request[3:8]
            File_Name_Length_decimal=(int(File_Name_Length,2))
            print(f"The lenght of the file is {File_Name_Length_decimal}")


            oldName=serversocket.recv(File_Name_Length_decimal-1).decode("utf-8")
            print(f"the old file name is : {oldName}")
            NewNameLength=serversocket.recv(8).decode()
            NewName=serversocket.recv(int(NewNameLength,2)-1).decode("utf-8")
            print(f"the new file name is : {NewName}")



            if os.path.exists(oldName):
                    
                # We receive the old name and the new name and ask the OS to change the name of the file using the OS modulte
                os.rename(oldName,NewName)

                print(f"The file has been changed from {oldName} to {NewName} ")
                serversocket.send(("00000000").encode())
                if Debug == 1:
                    print(f'The received request is {Op_code}')
                    print(f'The message sent is 00000000')
                    print(f'The name of the file received is {oldName}')
                    print(f'The file name lenght received is {File_Name_Length}')
                    print(f'The new file name sent is {NewName}')
            
            else : 
                
                serversocket.send(("11000000").encode())
                print("The file to change does not exist ")
                if Debug == 1:
                    print(f'The received request is {Op_code}')
                    print(f'The message sent is 11000000')
        
        elif Op_code=="111":

            serversocket.send(("01100000").encode())
            if Debug == 1:
                    print(f'The received request is {Op_code}')
                    print(f'The message sent is 01100000')

            

            






