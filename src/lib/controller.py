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
        self.intf = None
        self.sniffer = None

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
                    self.intf = i
                    return i

    def start(self):
        self.sniffer = AsyncSniffer(
            prn=lambda pkt: self.process(pkt), store=False, iface=self.get_intf()
        )
        self.sniffer.start()
        try:
            while True:
                pass
        except InterruptedError:
            self.sniffer.stop()

    def stop(self):
        self.sniffer.stop()
        exit()


if __name__ == "__main__":
    controller = Controller("ctrl")
    controller.start()
