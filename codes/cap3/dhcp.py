#!/usr/bin/python

# autor: Ramon dos Reis Fontes
# book: Wireless Network Emulation with Mininet-WiFi
# github: https://github.com/ramonfontes/mn-wifi-book-en

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='0/0', position='30,60,0')
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
                             position='50,50,0', failMode='standalone')
    h1 = net.addHost('h1', ip='192.168.11.1/24', inNamespace=False)

    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, h1)

    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    ap1.start([])

    h1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

