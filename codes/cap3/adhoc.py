#!/usr/bin/python

# autor: Ramon dos Reis Fontes
# book: Wireless Network Emulation with Mininet-WiFi
# github: https://github.com/ramonfontes/mn-wifi-book-en

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(autoTxPower):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    if autoTxPower:
        sta1 = net.addStation('sta1', position='10,10,0', range=100)
        sta2 = net.addStation('sta2', position='50,10,0', range=100)
        sta3 = net.addStation('sta3', position='90,10,0', range=100)
    else:
        sta1 = net.addStation('sta1', position='10,10,0')
        sta2 = net.addStation('sta2', position='50,10,0')
        sta3 = net.addStation('sta3', position='90,10,0')

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(sta1, intf='sta1-wlan0', cls=adhoc, ssid='adhocNet',
                mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta2, intf='sta2-wlan0', cls=adhoc, ssid='adhocNet',
                mode='g', channel=5)
    net.addLink(sta3, intf='sta3-wlan0', cls=adhoc, ssid='adhocNet',
                mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    autoTxPower = True if '-a' in sys.argv else False
    topology(autoTxPower)
