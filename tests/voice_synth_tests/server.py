import socket
import sys
import os

def listen_to_homie():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print ('listening for homie on {} port {}'.format(server_address[0], server_address[1]))
    sock.bind(server_address)

    sock.listen(1)
    print('waiting for a connection')
    connection, client_address = sock.accept();
    try:
        print ('connection from', client_address)
        f = open("recv.wav", "wb")
        data = connection.recv(1024)
        # Receive the data in small chunks and retransmit it
        while(data):
            size = sys.getsizeof(data)
            f.write(data)
            data = connection.recv(1024)
        print("finished writing to file recv.wav")
        f.close()
        print("size of file is {} bytes".format((os.stat("recv.wav")).st_size))
    finally:
        # Clean up the connection
        connection.close()
