
# host server for micropython to send data to. 
# not expected to run on micropython


import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5) 

print('Listening on {}:{}'.format(bind_ip, bind_port))

while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    request = client_sock.recv(1024)
    print('Received {}'.format(request))
    client_sock.send(bytes('ACK!1............................................', 'utf8'))
    client_sock.send(bytes('ACK!2............................................', 'utf8'))
    client_sock.send(bytes('ACK!3............................................', 'utf8'))
    client_sock.send(bytes('ACK!4............................................', 'utf8'))
    client_sock.send(bytes('ACK!5............................................', 'utf8'))
    client_sock.close()
