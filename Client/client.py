import socket

#This end string represent the student id of one of us. This is purely to verify that we have come to the end of the file . 
end_string=b"<40097236>"



#Asking the user to input the Clients IP and Port 
print("Welcome to the client side, please tell us which IP Address and port number you would like to Access")
Ip=input("IP: ")
Port=int(input("Port: "))
# # Ip="127.0.1.1"
# Port=9999


#-------Creating connection patterns for the client to connect to the server.-------------------- 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

Connection =(Ip,Port)
client.connect(Connection)
#-------------------Making sure the connection worked------------------------------------- 
Connection_Message=client.recv(1024)
print(Connection_Message.decode("utf-8"))   

Debug = int(input('Do you wish to be in debug mode (1 -> yes / 0-> no) :  '))

#----- Now that the connection has been confirmed, we ask the user to input what we need;-----------
while True:
  
    
   # Available commands : Help, BYE, PUT file.txt, GET file.txt, Change Text1.txt Text2.txt
    Option= input('\nPlease input which request you would like to send: ')
    if Option.upper() == "BYE": 
        #send a BYE request
        client.shutdown(2)
        client.close()
        break
        
    elif Option.upper() == "HELP":
        #Send a HELP request
        TempEncodingByte = "01100000"
        client.sendall(TempEncodingByte.encode())
        print(f"The Help request has been successfully sent.")
        #This Received Request is the reception of the message sent by the Server with the information to display. 
        ReceivedRequest=client.recv(8).decode()
        if ReceivedRequest[0:3]=="110":
            length=ReceivedRequest[3:]
            Data=client.recv(int(length,2)).decode()
            print(Data)
        if Debug == 1:
            print("----------------------THE FOLLOWING MESSAGES ARE PART OF THE DEBUG CONFIG------------------")
            print(f"The request sent is {TempEncodingByte}")
            print(f'The received message is {ReceivedRequest}')


    
# the else has been decided this way since the first 2 option do not require any FileName, therefore they are easy to parse as command. The next command need special parsing.
    else :


        index_for_space=Option.find(" ") #This parses the input for the first part of the request 
        index=Option.find(".") #returns the index of where the first . is (for the extension)
        Request=Option[0:index_for_space]  # This return only the request [PUT,CHANGE,GET]
        
        if Request.upper() == "PUT" :
            #Send a PUT request

            #-------We need to separate the name of the file with its extension-------------------
            Name_of_file=Option[(index_for_space+1):index] # Start after the space, end at the "." 
            Extension=Option[index:]            #start at the point, finish at the end of the String


            FileNameLength=bin(len(Name_of_file+Extension)+1) # We get the lenght of the file name , the bin commands is to have a binary representation(abstraction) of the length. We need it for the opcode

            TempEncodingByte= "000" + FileNameLength[2:] # Concatunating the Opcode and the Lenght in a binary representation 

            #print(TempEncodingByte) # ->> (OPP CODE FOR PUT + 10 ) --> 00001010

             
            print("Name of file : " + Name_of_file + "     Extension : " + Extension )


            #This While loop is only to make sure our bit representation has 8 bits. We appended 0's at the beggining. 
            while len(TempEncodingByte)<8:
               TempEncodingByte="0"+TempEncodingByte
            
            #---- We need to then open a file from our directory and be ready to send it to the server , the upload process----
            

            with open(Name_of_file+Extension, 'rb') as file:  # We open it as a read byte since we need to stream that data
                data=file.read()
        
             #----------Sending the required file through the tcp Server:----------------------------
            
            
            client.sendall(TempEncodingByte.encode())  # Sending Op code + file name lenght
            client.sendall((Name_of_file+Extension).encode())#Sending Name
            client.sendall(data) #Sending content of file 
            client.sendall(end_string) #Custom ending to know that we  have reached the ending. 
            
            print(f"The file : {Name_of_file} has been successfully uploaded to the server.")
            
            Reponse=client.recv(8).decode()[0:3] 
            if Reponse=="000":
                
                print(f"The File was succesfully uploaded on the server with response Op_code {Reponse} ")
            
            if Debug == 1:
                print("----------------------THE FOLLOWING MESSAGES ARE PART OF THE DEBUG CONFIG------------------")
                print(f'The request sent is {TempEncodingByte}')
                print(f'The name of the file sent is{Name_of_file+Extension}')
                print(f'The received message is {Reponse}')





        elif Request.upper() == "GET" :
        
            #-------We need to separate the name of the file with its extension-------------------
            Name_of_file=Option[(index_for_space+1):index]
            Extension=Option[index:]            
            FileNameLength=bin(len(Name_of_file+Extension)+1)            
            #print(TempEncodingByte) # ->> (OPP CODE FOR PUT + 10 ) --> 10001010
            print("Name of file : " + Name_of_file + "     Extension : " + Extension )
            realFileNameLength=FileNameLength[2:]
            while len(realFileNameLength)<5:
                realFileNameLength="0"+realFileNameLength

            TempEncodingByte= "001" + realFileNameLength

            #---- We need to then open a file from our directory and be ready to send it to the server , the upload process----

            print(f"The current client has asked to fetch {Name_of_file} from the server ") 
            client.sendall(TempEncodingByte.encode())
            client.sendall((Name_of_file + Extension).encode())
            





#---------------------------------RESPONSE MESSAGE FROM THE GET COMMAND -------------------------------------------------
            file_bytes=b""
            #Setting a flag for end of transfer: 
            Finished=False

            ReceivedResponse=client.recv(8).decode()
            ReceivedOpCode=ReceivedResponse[0:3]

            if ReceivedOpCode=="001":
                ReceivedFileNameLength=ReceivedResponse[3:]

                ReceivedFileName=client.recv(int(ReceivedFileNameLength,2)).decode()
                file=open(ReceivedFileName,"wb") ## Open a file with the name of the file passed , and then we will write into it any data bytes that we need 

                while not Finished:
                    data_received=client.recv(1024)
                    
                    file_bytes+=data_received
                    if file_bytes[-10:] == b"<40097236>":
                        Finished = True
                        print("The File has been properly received")
                    
                file.write(file_bytes[0:-10])
                file.close()
                print("The transfer of the file is finished")    
                if Debug == 1:
                    print("----------------------THE FOLLOWING MESSAGES ARE PART OF THE DEBUG CONFIG------------------")
                    print(f'The request sent is {TempEncodingByte}')
                    print(f'The name of the file sent is{Name_of_file+Extension}')
                    print(f'The received message is {ReceivedOpCode}')
                    print(f'The received response is {ReceivedResponse}')
                    print(f'The received file lenght is {ReceivedFileNameLength}')

            else: 
                print(f"The File requested does not exist , error code {ReceivedOpCode}")

            
            


        elif Request.upper() == "CHANGE" :

            #Creating an array that will store both full text file, since we split with the split function i
            DifferentFiles=Option[(index_for_space+1):].split(" ")
            Firstfile=DifferentFiles[0].split(".") #Same principle , we separate the name of the file with its extension
            SecondFile=DifferentFiles[1].split(".")#Same principle , we separate the name of the file with its extension

            Name_of_first_file=Firstfile[0]
            Extension_of_first_file="."+Firstfile[1]
            #We then get the full name of the file + its extension
            
            #print(f"The name of the first file is : {Name_of_first_file}, and its extension is {Extension_of_first_file}")

            
            Name_of_Second_file=SecondFile[0]
            Extension_of_Second_file="."+SecondFile[1]

            #We then get the full name of the file + its extension
            #print(f"The name of the second file is : {Name_of_Second_file} and its extension is {Extension_of_Second_file}")
            

#----------------------------Now that we have the proper names of the files that we need to change we can implement the logic ------------------- 
            OpCode= "010"
            
            #---------------  Get the Length of the first file name -----------------
            First_fileNameLength=(bin(len(Name_of_first_file+Extension_of_first_file)+1))[2:]
            #-------Formating the length so we have a full 8 bits--------------
            while len(First_fileNameLength)<5:
                First_fileNameLength="0"+First_fileNameLength


            #--------------- Get the length of the second file name 
            Second_fileNameLength=(bin(len(Name_of_Second_file+Extension_of_Second_file)+1))[2:]  
            while len(Second_fileNameLength)<8:
                Second_fileNameLength="0"+Second_fileNameLength


            #-------Formating the length so we have a full 8 bits--------------
        
        
            FirstEncodingToSend=OpCode+First_fileNameLength        
            client.sendall(FirstEncodingToSend.encode()) # senfing the opp code + first file name length
            client.send((Name_of_first_file + Extension_of_first_file ) .encode()) #sending the name of the file with its extension           
            client.send(Second_fileNameLength.encode()) #Sending the length of the second file 
            client.send((Name_of_Second_file+Extension_of_Second_file).encode()) #Sending the name + extension of seocnd file 

            print(f"The request to change the name of the first file from {Name_of_first_file} to {Name_of_Second_file} has been sent to the server ")
            
            Reponse=client.recv(8).decode()[0:3] 
            if Reponse=="000":
                print(f"The Files name were succesfully changed on the server with response Op_code {Reponse} ")

                if Debug == 1:
                    print("----------------------THE FOLLOWING MESSAGES ARE PART OF THE DEBUG CONFIG------------------")
                    print(f'The request sent is {OpCode}')
                    print(f'The name of the first file sent is{Name_of_first_file + Extension_of_first_file}')
                    print(f'The first file name lenght sent is {First_fileNameLength }')
                    print(f'The name of the second file sent is{Name_of_Second_file+Extension_of_Second_file}')
                    print(f'The second file name lenght sent is {Second_fileNameLength }')
                    print(f'The received response is {Reponse}')


            else: 
                print("There was an error changing the file name. The file you requested for a change does not exist ")

        else:
            client.send("11100000".encode())


            a= client.recv(8).decode()

            if a[0:3]=="011":
                print("The Current Request is not supported ")



            continue
       



print("Thank you for using this service ")


