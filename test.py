import socket
import pickle
from log import *

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('192.168.0.21', 9999))
data = pickle.loads(s.recv(16384))
print(data[0])
for i in data[1]:
	print(i.op)
	print(i.time)
	print(i.node)
	print(i.value)
s.close()

