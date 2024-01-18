#! /usr/bin/python3

"""
Run with `python3 | tee -a output_hname.txt`
"""

import os
import sys

import psutil
from scapy.all import *
from scapy.layers.l2 import *

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.constants import *
from lib.headers import BARC, CEther, deparser
from lib.utils import *

src_addr = ["00"] * 6


def get_src_mac(hname):
    nics = psutil.net_if_addrs()[f"{hname}_eth0"]
    for interface in nics:
        if interface.family == 17:
            return interface.address


def test_bi(hname):
    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_I, BI=[HST_ID, 0x00, 0x00, 0x00, 0x00, 0x00])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    ls(frame)
    sendp(frame, iface=f"{hname}-eth0")
    print("\n\n")


def test_bpfs(hname):
    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[FAB_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    ls(frame)
    sendp(frame, iface=f"{hname}-eth0")
    print("\n\n")


def test_bprs(hname):
    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[RCK_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    ls(frame)
    sendp(frame, iface=f"{hname}-eth0")
    print("\n\n")


def test_bpss(hname):
    # make BARC frame
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC inquiry frame with the first
    # field in BI set to host identifier
    barc = BARC(S=BARC_P, BI=[SPN_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    ls(frame)
    sendp(frame, iface=f"{hname}-eth0")
    print("\n\n")


def listen(hname, sleep_time=10):
    def show(x):
        print("Received frames:")
        ls(x)
        print("\n\n")

    # start asynchronous sniffer to log replies
    t = AsyncSniffer(prn=lambda x: show(x), store=False, iface=f"{hname}-eth0")

    t.start()
    time.sleep(sleep_time)
    t.stop()
