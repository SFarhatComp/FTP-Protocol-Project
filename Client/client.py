import socket

end_string=b"<40097236>"


#-------Creating connection patterns for the client to connect to the server.-------------------- 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((socket.gethostname(),9999))

#-------------------Making sure the connection worked------------------------------------- 
Connection_Message=client.recv(1024)
print(Connection_Message.decode("utf-8"))   

#OP_CODES = {"PUT" : 0b100, 'GET': 0b101, 'CHANGE': 0b110, 'HELP': 0b111} First implementation using literal bits

#----- Now that the connection has been confirmed, we ask the user to input what we need;-----------

while True:

   # Available commands : Help, BYE, PUT file.txt, GET file.txt, Change Text1.txt Text2.txt
    Option= input('Please input which request you would like to send: ')
    if Option.upper() == "BYE": 
        #send a BYE request
        client.shutdown(1)
        client.close()
        break
        
    elif Option.upper() == "HELP":
        #Send a HELP request
        
        TempEncodingByte = "01100000"
        client.sendall(TempEncodingByte.encode())
        print(f"The Help request has been successfully sent.")

        ReceivedRequest=client.recv(1024)
        print(ReceivedRequest.decode("utf-8"))

        
    
    else :
        index_for_space=Option.find(" ") #This parses the input for the first part of the request 
        index=Option.find(".") #returns the index of where the first . is (for the extension)
        Request=Option[0:index_for_space]
        
        if Request.upper() == "PUT" :
            #Send a PUT request

            #-------We need to separate the name of the file with its extension-------------------
            Name_of_file=Option[(index_for_space+1):index]
            Extension=Option[index:]            


            FileNameLength=bin(len(Name_of_file+Extension)+1)


            TempEncodingByte= "000" + FileNameLength[2:]




            #print(TempEncodingByte) # ->> (OPP CODE FOR PUT + 10 ) --> 10001010

             
            print("Name of file : " + Name_of_file + "     Extension : " + Extension )


            while len(TempEncodingByte)<8:
               TempEncodingByte="0"+TempEncodingByte

            
            #---- We need to then open a file from our directory and be ready to send it to the server , the upload process----
            





            with open(Name_of_file+Extension, 'rb') as file:
                data=file.read()
            
        
             
             
             #----------Sending the required file through the tcp Server:----------------------------
            
            
            client.sendall(TempEncodingByte.encode())
            client.sendall((Name_of_file+"_copy"+Extension).encode())#Received Name
            client.sendall(data)
            client.sendall(end_string) #Concatenation of the data byte + custom ending to know that we  have reached the ending. 


            print(f"The file : {Name_of_file} has been successfully uploaded to the server.")



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

            file_bytes=b""
            #Setting a flag for end of transfer: 
            Finished=False
            
            file=open(Name_of_file + Extension,"wb") ## Open a file with the name of the file passed , and then we will write into it any data bytes that we need 

            while not Finished:
                data_received=client.recv(1024)
                #print(f"The Current Data received is {data_received}")
                #print(f"The current value of  File Byte is : {file_bytes}")
                file_bytes+=data_received
                if file_bytes[-10:] == b"<40097236>":
                    Finished = True
                    print("The File has been properly received")
                
            file.write(file_bytes[0:-10])
            file.close()
            print("The transfer of the file is finished")    




        elif Request.upper() == "CHANGE" :
            DifferentFiles=Option[(index_for_space+1):].split(" ")
            Firstfile=DifferentFiles[0].split(".") 
            SecondFile=DifferentFiles[1].split(".")


            
            Name_of_first_file=Firstfile[0]
            Extension_of_first_file="."+Firstfile[1]

            
            print(f"The name of the first file is : {Name_of_first_file}, and its extension is {Extension_of_first_file}")

            
            Name_of_Second_file=SecondFile[0]
            Extension_of_Second_file="."+SecondFile[1]

            print(f"The name of the second file is : {Name_of_Second_file} and its extension is {Extension_of_Second_file}")
            



            OpCode= "010"
            First_fileNameLength=(bin(len(Name_of_first_file+Extension_of_first_file)+1))[2:]

            while len(First_fileNameLength)<5:
                First_fileNameLength="0"+First_fileNameLength

            
            Second_fileNameLength=(bin(len(Name_of_Second_file+Extension_of_Second_file)+1))[2:]  

            while len(Second_fileNameLength)<8:
                Second_fileNameLength="0"+Second_fileNameLength

            print(Second_fileNameLength)
            

            FirstEncodingToSend=OpCode+First_fileNameLength

            client.sendall(FirstEncodingToSend.encode())
            client.send((Name_of_first_file + Extension_of_first_file ) .encode())            
            client.send(Second_fileNameLength.encode())
            client.send((Name_of_Second_file+Extension_of_Second_file).encode())


            print(f"The request to change the name of the first file from {Name_of_first_file} to {Name_of_Second_file} has been sent to the server ")

            #Everything working until here 5/12/2022
            













            # Extension=Option[index:]            
            # 

            # #print(TempEncodingByte) # ->> (OPP CODE FOR PUT + 10 ) --> 10001010
            # print("Name of file : " + Name_of_file + "     Extension : " + Extension )

            



            pass
        else:
            print("The request sent is not supported.")
            print (Request)
            continue




print("Thank you for using this service ")


