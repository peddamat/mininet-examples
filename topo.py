# coding=UTF-8
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost #cpu Related settings
from mininet.link import TCLink # addLink Related settings

from sys import exit  # pylint: disable=redefined-builtin

from mininet.util import quietRun
from mininet.log import error
from mininet.log import setLogLevel, info

setLogLevel('info')
net = Mininet(host=CPULimitedHost, link=TCLink) # If performance is not limited, the parameter is empty

# Create network node
c0 = net.addController()
h1 = net.addHost('h1', cpu=0.5) #cpu Performance limitations
h2 = net.addHost('h2', cpu=0.5) #cpu Performance limitations
s1 = net.addSwitch('s1')

# Creating links between nodes
net.addLink(h1, s1)
net.addLink(h2, s1)

# Configure host ip
h1.setIP('10.0.0.1', 24)
h2.setIP('10.0.0.2', 24)


net.start()

h1.cmdPrint('sysctl net.ipv4.icmp_echo_ignore_broadcasts=0')
h2.cmdPrint('sysctl net.ipv4.icmp_echo_ignore_broadcasts=0')

h1.cmdPrint('route add -net 224.0.0.0 netmask 240.0.0.0 dev h1-eth0')
h2.cmdPrint('route add -net 224.0.0.0 netmask 240.0.0.0 dev h2-eth0')

h1.cmdPrint('ip addr add 224.0.0.2/32 dev h1-eth0 autojoin')
h2.cmdPrint('ip addr add 224.0.0.2/32 dev h2-eth0 autojoin')

h1.cmdPrint('ip maddr show')
h2.cmdPrint('ip maddr show')

print('\n*** Setup complete!')
print('*** Try: h1 ping -I h1-eth0 224.0.0.2\n')

CLI( net)

net.stop()
