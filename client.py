import socket
import os

class client:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def connect_server(self):
        self.client_socket.connect((self.ip,self.port))
        print(self.client_socket.recv(1024).decode())
        self.init_response()
    
    def init_response(self):
        operation = str(input("What operation do you want to use? (Download/Upload)")).lower()
        self.client_socket.send(operation.encode())
        if(operation == "upload"):
            file_name = str(input("Input file name here: "))
            self.upload_file(file_name)
        elif(operation == "download"):
            self.download_file()
        else:
            print("Invalid input. Please try again🫰🏽")
            self.init_response() 

    def upload_file(self,file_name):
        self.client_socket.send(file_name.encode())
        file = open(file_name,"rb")
        data=file.read()
        self.client_socket.sendall(data)
        self.client_socket.send(b"<END>")
    
    def download_file(self):
        #path = str(input("Where do you want to save the file? "))
        print(self.client_socket.recv(1024).decode())
        file_name = str(input(""))
        self.client_socket.send(file_name.encode())
        path = "C:/Users/porat/Downloads/file_server/Files_download"
        file = open(path + f"/{file_name}", "wb")
        bytes_file = b""
        finished= False
        while not finished:
            data=self.client_socket.recv(1024)
            if data[-5:] == "<END>".encode():
                bytes_file += data
                finished = True
            else:
                bytes_file += data
        file.write(bytes_file[:-5])
        file.close()

my_client = client('127.0.0.1',1234)
my_client.connect_server()
