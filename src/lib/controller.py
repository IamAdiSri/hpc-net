import os
import sys

import psutil
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from scapy.all import AsyncSniffer

sys.path.append(os.path.join(sys.path[0], ".."))
from lib.headers import deparser


class Controller:
    def __init__(self, name, thrift_ip=None):
        self.name = name
        self.thrift_ip = "127.0.0.1" if not thrift_ip else thrift_ip
        self.intf = []
        self.sniffer = []

    def process(self, pkt):
        pkt = deparser(pkt)
        pkt.show()

    def get_intf(self):
        if self.intf:
            return self.intf
        else:
            addrs = psutil.net_if_addrs()
            for i in addrs.keys():
                if self.name in i:
                    self.intf.append(i)
            return self.intf

    def start(self):
        for intf in self.get_intf():
            self.sniffer.append(
                AsyncSniffer(prn=lambda pkt: self.process(pkt), store=False, iface=intf)
            )
            self.sniffer[-1].start()
        try:
            while True:
                pass
        except Exception:
            self.stop()

    def stop(self):
        for t in self.sniffer:
            t.stop()
        exit()


if __name__ == "__main__":
    controller = Controller("ctrl")
    controller.start()
