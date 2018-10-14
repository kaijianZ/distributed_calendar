import socket
import pickle
import os.path
from log import *

STABLE_STORAGE = 'logs.pkl'

def load_log(all_logs):
	if os.path.isfile(STABLE_STORAGE) is True:
		with open(STABLE_STORAGE, 'rb') as input:
			all_logs = pickle.load(input)
			# print_logs(all_logs)
		return True
	else:
		return False
  

def dump_log(all_logs):
	with open(STABLE_STORAGE, 'wb') as output:
		pickle.dump(all_logs, output, pickle.HIGHEST_PROTOCOL)
	

def print_logs(all_logs):
	for i in all_logs:
		print(f'operation: {i.op}')
		print(f'matrix clock: {i.time}')
		print(f'node: {i.node}')
		print(f'value: {i.value}')


if __name__ == "__main__":
	""" restore log """
	all_logs = []
	load_log(all_logs)

	""" receive log """
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('192.168.0.21', 9999))
	data = pickle.loads(s.recv(16384))
	for i in data[1]:
		alog = Log(i.op, i.time, i.node, i.value)
		all_logs.append(alog)

	print(data[0])
	print(all_logs)

	""" update log """
	dump_log(all_logs)

	for i in range(4): 
		print('.')

	s.close()
	
	