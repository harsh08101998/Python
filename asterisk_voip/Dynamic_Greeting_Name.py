import socket, requests
from numpy import heaviside
from encutils import encodingByMediaType
import csv,json,base64
# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024)
    print(request)
    # main_number=request[57:67]
    # print(main_number)
    # listt=request.
    # callfrom=listt[20,30]
    # print(request[47,20])
    # request.
    # with open("harshkumar.csv",'r  as file2:
    #     file_reader= csv.DictReader(file2)
    #     for i in file_reader:
    #         number=i['ID']
    #         print(number)
    #         if number == main_number:
    #             show=i['Name']
            


    response = "Heelo Harsh"
    client_connection.sendall('Thank you for connecting'.encode())


    client_connection.close()

# Close socket
server_socket.close()
