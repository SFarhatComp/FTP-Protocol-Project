# COEN366Project
TCP Socket FTP Protocol
This repository contains a Python implementation of a TCP Socket FTP (File Transfer Protocol) protocol. The code allows a client to connect to a server and perform various operations such as GET, PUT, CHANGE, BYE, and HELP commands.

Features
The TCP Socket FTP protocol implementation offers the following features:

Connection Establishment: The client can establish a TCP socket connection with the server using the specified host IP address and port number.

GET Command: The client can request a file from the server using the GET command. The server responds by sending the requested file to the client.

PUT Command: The client can upload a file to the server using the PUT command. The server receives the file and stores it in the appropriate directory.

CHANGE Command: The client can change the current working directory on the server using the CHANGE command. This allows the client to navigate through the server's file system.

BYE Command: The client can gracefully terminate the connection with the server using the BYE command. This ensures the release of network resources and proper closure of the connection.

HELP Command: The client can request a list of available commands and their usage using the HELP command. The server responds by providing information about the supported commands.
