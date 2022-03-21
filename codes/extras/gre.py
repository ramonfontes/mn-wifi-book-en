#!/usr/bin/python

"""
   Example of GRE Tunnel
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


def topology():

    "Create a network."
    net = Mininet()

    print("*** Creating nodes")
    h1 = net.addHost('h1', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip='192.168.10.1/24')
    h3 = net.addHost('h3', mac='00:00:00:00:00:03', ip='192.168.10.2/24')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04', ip='192.168.10.3/24')
    h5 = net.addHost('h5', mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', mac='00:00:00:00:00:06', ip='192.168.20.1/24')
    h7 = net.addHost('h7', mac='00:00:00:00:00:07', ip='192.168.20.2/24')
    h8 = net.addHost('h8', mac='00:00:00:00:00:08', ip='192.168.20.3/24')
    h9 = net.addHost('h9', mac='00:00:00:00:00:09', ip='140.116.172.1/24')
    h10 = net.addHost('h10', mac='00:00:00:00:00:0A', ip='140.116.172.2/24')

    print("*** Creating links")
    net.addLink(h1, h2)
    net.addLink(h1, h3, intfName1='h1-eth1')
    net.addLink(h1, h4, intfName1='h1-eth2')
    net.addLink(h5, h6)
    net.addLink(h5, h7, intfName1='h5-eth1')
    net.addLink(h5, h8, intfName1='h5-eth2')
    net.addLink(h9, h10)
    net.addLink(h9, h1, intfName1='h9-eth1', intfName2='h1-eth3')
    net.addLink(h10, h5, intfName1='h10-eth1', intfName2='h5-eth3')

    print("*** Building network")
    net.build()

    print("*** Adding some commands")
    h1.cmd("sudo ifconfig h1-eth0 0")
    h1.cmd("sudo ifconfig h1-eth1 0")
    h1.cmd("sudo ifconfig h1-eth2 0")
    h1.cmd("sudo ifconfig h1-eth3 0")
    h1.cmd("sudo brctl addbr mybr")
    h1.cmd("sudo brctl addif mybr h1-eth0")
    h1.cmd("sudo brctl addif mybr h1-eth1")
    h1.cmd("sudo brctl addif mybr h1-eth2")
    h1.cmd("sudo brctl addif mybr h1-eth3")
    h1.cmd("sudo ifconfig mybr up")
    h5.cmd("sudo ifconfig h5-eth0 0")
    h5.cmd("sudo ifconfig h5-eth1 0")
    h5.cmd("sudo ifconfig h5-eth2 0")
    h5.cmd("sudo ifconfig h5-eth3 0")
    h5.cmd("sudo brctl addbr mybr2")
    h5.cmd("sudo brctl addif mybr2 h5-eth0")
    h5.cmd("sudo brctl addif mybr2 h5-eth1")
    h5.cmd("sudo brctl addif mybr2 h5-eth2")
    h5.cmd("sudo brctl addif mybr2 h5-eth3")
    h5.cmd("sudo ifconfig mybr2 up")
    h9.cmd("sudo echo 1 > /proc/sys/net/ipv4/ip_forward")
    h10.cmd("sudo echo 1 > /proc/sys/net/ipv4/ip_forward")
    h9.cmd("sudo ifconfig h9-eth1 192.168.10.254 netmask 255.255.255.0")
    h10.cmd("sudo ifconfig h10-eth1 192.168.20.254 netmask 255.255.255.0")

    # No NAT setting: 192.168.10.0/24 can not talk to 192.168.20.0
    # configure gre tunnel
    h9.cmd("sudo ip tunnel add netb mode gre remote 140.116.172.2 local 140.116.172.1 ttl 255")
    h9.cmd("sudo ip addr add 192.168.10.253 dev netb")
    h9.cmd("sudo ifconfig netb up")
    h9.cmd("sudo ip route add 192.168.20.0/24 via 192.168.10.253")
    h10.cmd("sudo ip tunnel add neta mode gre remote 140.116.172.1 local 140.116.172.2 ttl 255")
    h10.cmd("sudo ip addr add 192.168.20.253 dev neta")
    h10.cmd("sudo ifconfig neta up")
    h10.cmd("sudo ip route add 192.168.10.0/24 via 192.168.20.253")
    h2.cmd("sudo ip route add 192.168.20.0/24 via 192.168.10.253")
    h3.cmd("sudo ip route add 192.168.20.0/24 via 192.168.10.253")
    h4.cmd("sudo ip route add 192.168.20.0/24 via 192.168.10.253")
    h6.cmd("sudo ip route add 192.168.10.0/24 via 192.168.20.253")
    h7.cmd("sudo ip route add 192.168.10.0/24 via 192.168.20.253")
    h8.cmd("sudo ip route add 192.168.10.0/24 via 192.168.20.253")

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
