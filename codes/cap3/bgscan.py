#!/usr/bin/python

# autor: Ramon dos Reis Fontes
# book: Wireless Network Emulation with Mininet-WiFi
# github: https://github.com/ramonfontes/mn-wifi-book-en

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import UserAP
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    net.addStation('sta1', position='15,20,0', bgscan_threshold=-60,
                   s_inverval=5, l_interval=10)
    ap1 = net.addAccessPoint('ap1', mac='00:00:00:00:00:01', ssid="handover",
                             mode="g", channel="1", passwd='123456789a',
                             encrypt='wpa2', position='10,30,0')
    ap2 = net.addAccessPoint('ap2', mac='00:00:00:00:00:02', ssid="handover",
                             mode="g", channel="6", passwd='123456789a',
                             encrypt='wpa2', position='60,30,0')
    ap3 = net.addAccessPoint('ap3', mac='00:00:00:00:00:03', ssid="handover",
                             mode="g", channel="1", passwd='123456789a',
                             encrypt='wpa2', position='120,100,0')
    c1 = net.addController('c1')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)

    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
