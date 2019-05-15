import socket
import sys

def ones_complement(n):
    one = ""
    for c in n:
        if c == "0":
            one += "1"
        else:
            one += "0"
    return one

server = socket.socket()
server.bind(('192.168.50.234', 12345))
server.listen(1)
checksumSize = 16

while True:
    connection, addr = server.accept()
    msg = input("Enter message : ")
    if len(msg) % checksumSize != 0:
        msg += "0" * (checksumSize - len(msg) % checksumSize)
        print("After padding : " + msg)
    checksum = 0
    j = 0
    for i in range(checksumSize, len(msg)+1, checksumSize):
        checksum += int(msg[j:i], 2)
        j += checksumSize
    checksumB = str("{0:b}".format(checksum))
    if len(checksumB) > checksumSize:
        e = len(checksumB) - checksumSize
        checksum = int(checksumB[0:e], 2) + int(checksumB[e:], 2)
    checksumB = str("{0:b}".format(checksum))
    if len(checksumB) < checksumSize:
        checksumB = "0" * (checksumSize - len(checksumB)) + checksumB
    checksumB = ones_complement(checksumB)
    print("Binary Checksum : " + checksumB)
    print("Checksum : " + str(int(checksumB, 2)))
    connection.send((msg + checksumB).encode('utf-8'))
    ack = connection.recv(1024)
    if ack.decode('utf-8') == "ACK":
        print("Message successfully received by client")
        break
    else:
        print("Error")
server.close()
sys.exit()
