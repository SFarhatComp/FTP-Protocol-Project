import socket

end_string=b"<40097236>"


#-------Creating connection patterns for the client to connect to the server.-------------------- 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((socket.gethostname(),9999))

#-------------------Making sure the connection worked------------------------------------- 
Connection_Message=client.recv(1024)
print(Connection_Message.decode("utf-8"))



#----- Now that the connection has been confirmed, we ask the user to input what we need;-----------



while True:

   # Available commands : Help, BYE, PUT file.txt, GET file.txt, Change Text1.txt Text2.txt

    Option= input('Please input which request you would like to send: ')

    if Option.upper() == "BYE": 
        #send a BYE request
        client.close()
        
    
    elif Option.upper() == "HELP":
        #Send a HELP request
        pass
    
    else :

        index_for_space=Option.find(" ") #This parses the input for the first part of the request 
        index=Option.find(".") #returns the index of where the first . is (for the extension)
        Request=Option[0:index_for_space]
        
    

    
        if Request.upper() == "PUT" :
            #Send a PUT request


            #-------We need to separate the name of the file with its extension-------------------
            Name_of_file=Option[(index_for_space+1):index]
            Extension=Option[index:]

            ##
            
        
            FileNameLength=bin(len(Name_of_file+Extension)+1)
            TempEncodingByte="000"+FileNameLength[2:]
            print("Name of file : " + Name_of_file + "     Extension : " + Extension )

            while len(TempEncodingByte)<8:
                TempEncodingByte="0"+TempEncodingByte

            
             #------ We need to then open a file from our directory and be ready to send it to the server , the upload process----
            
            file = open(Name_of_file+Extension,"rb") #open the file as a read bytes
            
            data=file.read()
             #This is an ending tag that represent my student ID , this will allow me to make sure that the complete message was sent 
            
             #----------Sending the required file through the tcp Server:----------------------------
            
            
            client.send(TempEncodingByte.encode())
            client.send((Name_of_file+"_copy"+Extension).encode())#Received Name

            client.sendall(data)
            client.send(end_string) #Concatenation of the data byte + custom ending to know that we  have reached the ending. 
            file.close()
            #Once we have finished manipulating the data, we can then close the file . 

            print(f"The file : {Name_of_file} has been successfully uploaded to the server.")



        elif Request.upper() == "GET" :
            #Send a GET request
            pass

        elif Request.upper() == "Change" :
            #Send a CHANGE request
            pass
        else:
            print("The request sent is not supported.")
            print (Request)
            continue




print("Thank you for using this service ")
