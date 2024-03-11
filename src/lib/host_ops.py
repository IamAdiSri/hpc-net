# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import random
import sys

import psutil
from scapy.all import *
from scapy.layers.l2 import *

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.constants import *
from lib.headers import BARC, CORE, CEther, deparser
from lib.utils import *

src_addr = None
intf = None
captures = []


def get_intf():
    """
    Get network interface
    """

    global intf
    if intf:
        return intf
    else:
        addrs = psutil.net_if_addrs()
        for i in addrs.keys():
            if "h_" in i:
                intf = i
                return i


def get_src_addr(intf=get_intf()):
    """
    Generate a random source address
    unless source address has already
    been recorded (needed for tracking
    packets)
    """

    global src_addr
    if not src_addr:
        try:
            with open(f"../emulation/outputs/addr_{intf.split('-')[0]}", "r") as f:
                src_addr = f.read()
        except:
            temp_src_addr = "ae:"
            while len(temp_src_addr) < 15:
                temp_src_addr += hex(random.randint(0, 15))[2:]
                temp_src_addr += hex(random.randint(0, 15))[2:]
                temp_src_addr += ":"
            temp_src_addr += hex(random.randint(0, 15))[2:]
            temp_src_addr += hex(random.randint(0, 15))[2:]
            return temp_src_addr
    return src_addr


def test_bi(intf=get_intf()):
    """
    Test BARC inquiry
    """

    # make CEther frame with dest MAC set to
    # NCB address and etherType
    # set to BARC identifier
    ether = CEther(dst=xtos(NCB_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_I, BI=[HST_ID, 0x00, 0x00, 0x00, 0x00, 0x00])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def test_bprs(intf=get_intf()):
    """
    Test BARC proposal to rack switch
    """

    # make CEther frame with dest MAC set to
    # NCB address and etherType
    # set to BARC identifier
    ether = CEther(dst=xtos(NCB_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[RCK_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def test_bpfs(intf=get_intf()):
    """
    Test BARC proposal to fabric switch
    """

    # make CEther frame with dest MAC set to
    # NCB address and etherType
    # set to BARC identifier
    ether = CEther(dst=xtos(NCB_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[FAB_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def test_bpss(intf=get_intf()):
    """
    Test BARC proposal to spine switch
    """

    # make CEther frame with dest MAC set to
    # NCB address and etherType
    # set to BARC identifier
    ether = CEther(dst=xtos(NCB_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC inquiry frame with the first
    # field in BI set to host identifier
    barc = BARC(S=BARC_P, BI=[SPN_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def test_core(ca, intf=get_intf()):
    """
    Test Collective Registration
    """
    # make CEther frame with NCB address as destination
    # type as CORE type
    ether = CEther(dst=xtos(NCB_DA), src=get_src_addr(), type=TYPE_CORE)

    # make CORE frame
    core = CORE(
        CA=[int(f"0x{x}", 16) for x in ca.split(":")],
    )

    # compile and display complete frame
    frame = ether / core
    print("\nSending CEther/CORE frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def test_unicast(dst, intf=get_intf()):
    """
    Test Unicast message
    """

    # make UNIC frame
    ether = CEther(dst=dst, src=get_src_addr())

    # compile and display complete frame
    frame = ether / f"message from {intf.split('-')[0]}"
    print("\nSending UNICAST frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def test_multicast(dst, intf=get_intf()):
    """
    Test Multicast message
    """

    # make multicast frame
    ether = CEther(dst=dst, src=get_src_addr())

    # compile and display complete frame
    frame = ether / f"message from {intf.split('-')[0]}"
    print("\nSending MULTICAST frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n")


def listen(intf=get_intf()):
    """
    Listen for incoming packets
    """

    global src_addr

    def show(x):
        print("Received frame:")
        x = deparser(x)
        x.show()
        # ls(x)
        print("\n")

        if x.type == TYPE_BARC and x.S == BARC_P:
            src_addr = ":".join(["%02x" % a for a in x.BI])
            with open(f"outputs/addr_{intf.split('-')[0]}", "w") as f:
                f.write(src_addr)
            print(f"Updated self address: {src_addr}")

        captures.append(x)

    def lfilter(x):
        x = deparser(x)
        if x.type == TYPE_BARC and x.S == BARC_I:
            return False
        elif x.src == get_src_addr():
            return False
        return True

    # start asynchronous sniffer to log replies
    t = AsyncSniffer(prn=lambda x: show(x), store=False, iface=intf, lfilter=lfilter)

    t.start()

    return t
