# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Run with `python3 | tee -a output_hname.txt`

import argparse
import os
import sys
import time
import psutil

from scapy.all import *
from scapy.layers.l2 import *

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.constants import *
from lib.headers import BARC, CEther, UNIC, deparser
from lib.utils import *

def get_intf():
    addrs = psutil.net_if_addrs()
    for i in addrs.keys():
        if "hst" in i:
            return i
    return None

def get_src_addr(intf=get_intf()):
    try:
        with open(f"outputs/addr_{intf.split('-')[0]}", 'r') as f:
            src_addr = f.read()
        return src_addr
    except:
        src_addr = "00:00:00:00:00:00"


def test_bi(intf=get_intf()):
    """
    Test BARC inquiry
    """

    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_I, BI=[HST_ID, 0x00, 0x00, 0x00, 0x00, 0x00])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


def test_bprs(intf=get_intf()):
    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[RCK_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


def test_bpfs(intf=get_intf()):
    """
    Test BARC proposal to fabric switch
    """

    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[FAB_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


def test_bpss(intf=get_intf()):
    """
    Test BARC proposal to spine switch
    """

    # make BARC frame
    ether = CEther(dst=xtos(BARC_DA), src=get_src_addr(), type=TYPE_BARC)

    # make BARC inquiry frame with the first
    # field in BI set to host identifier
    barc = BARC(S=BARC_P, BI=[SPN_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")

def test_unicast(dst, intf=get_intf()):
    """
    Test Unicast message
    """

    # make UNIC frame
    ether = CEther(dst=dst, src=get_src_addr(), type=TYPE_UNIC)

    # compile and display complete frame
    frame = ether / f"message from {intf.split('-')[0]}"
    print("\nSending UNICAST frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


captures = []


def listen(intf=get_intf()):
    """
    Listen for incoming packets
    """

    def show(x):
        print("Received frames:")
        x = deparser(x)
        x.show()
        # ls(x)
        print("\n\n")

        if x.type == TYPE_BARC and x.S == BARC_P:
            src_addr = ":".join([str(a) for a in x.BI])
            with open(f"outputs/addr_{intf.split('-')[0]}", 'w') as f:
                f.write(src_addr)
            print(f"Updated self address: {src_addr}")

        captures.append(x)

    def lfilter(x):
        x = deparser(x)
        if x.type == TYPE_BARC and x.S == BARC_I:
            return False
        if x.type == TYPE_UNIC and x.src == get_src_addr():
            return False
        return True

    # start asynchronous sniffer to log replies
    t = AsyncSniffer(prn=lambda x: show(x), 
                     store=False, 
                     iface=intf,
                     lfilter=lfilter
        )

    t.start()

    return t


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="test.py", description="Run host traffic simulation"
    )
    parser.add_argument("interface", type=str)
    args = parser.parse_args()

    # start async sniffing
    listen(args.interface)

    # this timeout will need to be
    # increased for larger k values
    time.sleep(10)

    # send BARC initilization frame
    test_bi(args.interface)

    # this timeout will need to be
    # increased for larger k values
    time.sleep(10)
