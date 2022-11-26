import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((socket.gethostname(),9999))


#Creating connection patterns for the client to connect to the server. 
 
#Making sure the connection worked 
Connection_Message=client.recv(1024)
print(Connection_Message.decode("utf-8"))


# Now that the connection has been confirmed, we ask the user to input what we need,

file_to_be_implemented= input('What is the file that you would want to update : ')

# We need to then open a file from our directory and be ready to send it to the server , the upload process
file = open(file_to_be_implemented,"rb")
data=file.read()
end_string=b"<40097236>" #This is an ending tag that represent my student ID , this will allow me to make sure that the complete message was sent 




#We need to separate the name of the file with its extension
index=file_to_be_implemented.find(".")
Name_of_file=file_to_be_implemented[0:index]
Extension=file_to_be_implemented[index:]
print("Name of file : " + Name_of_file + "     Extension : " + Extension )





#Sending the required file through the tcp Server:
client.send((Name_of_file+"_copy"+Extension).encode())#Received Name
client.sendall(data+end_string)
file.close()

#Once we have finished getting the data, we can then close the file . 

print(f"The file : {file_to_be_implemented} has been successfully uploaded to the server.")
client.close()
#close the client















# full_msg=""
# while True:
#     msg=s.recv(1024)
#     if len(msg) <=0:
#         break

#     full_msg+=msg.decode("utf-8")
    
# print(full_msg)