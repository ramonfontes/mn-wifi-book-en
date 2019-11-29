#!/usr/bin/python

# autor: Ramon dos Reis Fontes
# book: Wireless Network Emulation with Mininet-WiFi
# github: https://github.com/ramonfontes/mn-wifi-book-en

from __future__ import print_function
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import adhoc


def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', wlans=2)
    sta2 = net.addStation('sta2')
    ap1 = net.addAccessPoint('ap1', ssid='ssid_1', mode='g', channel='5',
                             failMode="standalone")

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating...\n")
    net.addLink(ap1, sta1)
    net.addLink(sta1, intf='sta1-wlan0', cls=adhoc, ssid='adhoc1')
    net.addLink(sta2, intf='sta2-wlan0', cls=adhoc, ssid='adhoc1')

    info("*** Starting network\n")
    net.build()
    ap1.start([])

    info("*** Addressing...\n")
    sta1.setIP('192.168.10.1/24', intf="sta1-wlan1")
    sta2.setIP('192.168.10.2/24', intf="sta2-wlan0")

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
