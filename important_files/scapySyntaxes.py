from scapy.all import *

def sendAPacket():
    # This programs sends IP packets with a ttl of 64 hops and without any tcp or udp headers or body
    x = IP(ttl=64)      #ttl --> Time to Live
    x.src = "10.0.13.6"  # set the source IP
    x.dst = "10.0.12.120"     # set the destination IP
    send(x)
    # The above cab be done in a single line like below
    y = send(IP(ttl=4, src="10.0.13.6", dst="10.0.12.120"))

# sendAPacket()

def sendICMPPacket():
    # This program sends ICMP packets to the destinations adresss
    # This is how to write a onliner
    packet = IP(src="10.0.13.6", dst="10.0.12.120")/ICMP()/"Optional Body for ICMP"
    # A Forward Slash / will stack the previuos Layer with the next layer
    send(packet)

#sendICMPPacket()

def DOSAttack():
    # This fucntion will send huge amounts of packets to the specified port
    packet = IP(src="10.0.13.6", dst="10.0.12.120")/TCP(sport=80, dport=80)
    send(packet, count=10000)
    # However this doesn't seem to have an impact on the webserver because there
    # is no proper three way handshake

# DOSAttack()

def showLayers():
    #Inititalize Layer 2 (Data Link/Internet) and Layer 3 (Networking/Transport)
    Layer2 = Ether()
    Layer3 = IP()

    # Show the default contents of Layer 2 and Layer 3
    # Layer2.show()
    # Layer3.show()

    # Change the source MAC from Layer 2
    Layer2 = Ether(src="01:02:03:04:05:06")
    # Layer2.show()

    # If IP source and destination is not specified it will take the  loopback address as default

    # Change the surce IP Layer 3 
    Layer3 = IP(src="10.0.13.6")
    # Layer3.show()

    # Layer 4 (Application)
    Layer4 = TCP()
    # Layer4.show()

    stack = Layer2/Layer3/Layer4
    stack.show()
# showLayers()

