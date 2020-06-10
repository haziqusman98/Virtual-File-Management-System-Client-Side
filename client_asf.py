# Import socket module
import socket
import pickle
import fileSystem.main as filesystem

serv_ip = input("Enter server IP: ")
port = 12345


# Create a socket object
s = socket.socket()

# Define the port on which you want to connect

# connect to the server on local computer
s.connect((serv_ip, port))
d=pickle.loads(s.recv(8192))
filesystem.main(d, serv_ip, port)
s.close()




