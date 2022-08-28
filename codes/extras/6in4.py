#!/usr/bin/python

"""@author: Ramon Fontes
@email: ramon.fontes@imd.ufrn.br"""

from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.net import Mininet


def topology():
    "Create a network."
    net = Mininet()

    info("*** Creating nodes\n")
    h1 = net.addHost('h1', ip='10.0.0.1/8')
    h2 = net.addHost('h2', ip='192.168.0.1/24')
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')

    info("*** Creating Links\n")
    net.addLink(h1, r1)
    net.addLink(h2, r2)
    net.addLink(r1, r2)

    info("*** Starting network\n")
    net.build()

    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('sysctl net.ipv4.ip_forward=1')

    r1.cmd('sysctl net.ipv6.conf.all.forwarding=1')
    r2.cmd('sysctl net.ipv6.conf.all.forwarding=1')

    r1.cmd('ifconfig r1-eth0 10.0.0.2/8')
    r2.cmd('ifconfig r2-eth0 192.168.0.2/24')

    r1.cmd('ifconfig r1-eth1 172.16.0.1/30')
    r2.cmd('ifconfig r2-eth1 172.16.0.2/30')
    r1.cmd('route add -net 192.168.0.0/24 gw 172.16.0.2')
    r2.cmd('route add -net 10.0.0.0/8 gw 172.16.0.1')

    h1.cmd('ip -6 addr add 2001::2/64 dev h1-eth0')
    h2.cmd('ip -6 addr add 2002::2/64 dev h2-eth0')

    r1.cmd('ip -6 addr add 2001::1/64 dev r1-eth0')
    r2.cmd('ip -6 addr add 2002::1/64 dev r2-eth0')

    r1.cmd('ip tunnel add tun6to4 mode sit ttl 254 local 172.16.0.1 remote 172.16.0.2')
    r1.cmd('ip link set dev tun6to4 up')
    r1.cmd('ip addr add 2005::1/64 dev tun6to4')
    r1.cmd('ip route add 2002::/64 via 2005::2')

    r2.cmd('ip tunnel add tun6to4 mode sit ttl 254 local 172.16.0.2 remote 172.16.0.1')
    r2.cmd('ip link set dev tun6to4 up')
    r2.cmd('ip addr add 2005::2/64 dev tun6to4')
    r2.cmd('ip route add 2001::/64 via 2005::1')

    h1.cmd('ip -6 route add 2002::2 via 2001::1')
    h2.cmd('ip -6 route add 2001::2 via 2002::1')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
