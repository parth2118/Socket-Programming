import socket
import sys
import math

def ones_complement(n):
    number_of_bits = int(math.floor(math.log(n)/math.log(2))) + 1
    return ((1 << number_of_bits) - 1) ^ n

s = socket.socket()
s.connect(('192.168.50.234', 12345))
checksumSize = 16

while True:
    msg = s.recv(1024)
    print("Message Received : " + msg.decode('utf-8'))
    checksum = 0
    j = 0
    for i in range(checksumSize, len(msg)+1, checksumSize):
        checksum += int(msg[j:i], 2)
        j += checksumSize
    checksumB = str("{0:b}".format(checksum))
    if len(checksumB) > 16:
        e = len(checksumB) - 16
        checksum = int(checksumB[0:e], 2) + int(checksumB[e:], 2)
    print("Binary Checksum : " + str("{0:b}".format(checksum)))
    print("Checksum Calculated : " + str(checksum))
    if ones_complement(checksum) == 0:
        print("No Error in message")
        s.send("ACK".encode('utf-8'))
        break
    else:
        print("Error in received message")
        s.send("NACK".encode('utf-8'))
s.close()
sys.exit()
