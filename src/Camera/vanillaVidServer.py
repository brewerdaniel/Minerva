import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 1234))
server_socket.listen(5)
import os,time

data="hey"

client_socket, address = server_socket.accept()
print "Conencted to - ",address,"\n"
while (1):
    data = client_socket.recv(1024)
    print "The following data was received - ",data
    print "Opening file - ",data
    strt=time.time()
    img = open(data,'r')
    while True:
        strng = img.readline(512)
        if not strng:
            break
        client_socket.send(strng)
    img.close()
    client_socket.close()
    print "Data sent successfully in ", time.time()-strt, "s"
    #exit()
        #data = 'viewnior '+data
        #os.system(data)
