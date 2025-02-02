import socket
import os

class server:
    def __init__(self,port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a socket type TCP 
        self.server_socket.bind(('',port))

    def start_listen(self):
        while True:
            self.server_socket.listen(5)
            client , addr = self.server_socket.accept()
            client.send(("I'm listening").encode())
            self.init_repsonse(client)
        self.server_socket.close()

    def init_repsonse(self,client):
        operation = client.recv(1024).decode()
        if(operation == "upload"):
            self.receive_file(client)
        elif(operation == "download"):
            self.transfer_file(client)

    def receive_file(self,client):
        file_name = client.recv(1024).decode()
        file = open(f"C:/Users/porat/Downloads/file_server/Files_upload/{file_name}", "wb")
        bytes_file = b""
        finished = False
        while not finished:
            data=client.recv(1024)
            if data[-5:] == "<END>".encode():
                bytes_file += data
                finished = True
            else:
                bytes_file += data
        file.write(bytes_file)
        file.close()

    def transfer_file(self,client):
        client.send((f"Input your chosen file: {os.listdir("C:/Users/porat/Downloads/file_server/Files_upload")}").encode())
        file_name = (client.recv(1024)).decode()
        file = open(f"C:/Users/porat/Downloads/file_server/Files_upload/{file_name}","rb")
        data=file.read()
        client.sendall(data)
        client.send(b"<END>")
    
my_server = server(1234)

my_server.start_listen()

