# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Run with `python3 | tee -a output_hname.txt`

import os
import sys
import argparse
import time

from scapy.all import *
from scapy.layers.l2 import *

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.constants import *
from lib.headers import BARC, CEther, deparser
from lib.utils import *

src_addr = ["00"] * 6


def test_bi(intf):
    """
    Test BARC inquiry
    """

    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_I, BI=[HST_ID, 0x00, 0x00, 0x00, 0x00, 0x00])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


def test_bprs(intf):
    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[RCK_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


def test_bpfs(intf):
    """
    Test BARC proposal to fabric switch
    """

    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

    # make BARC frame
    barc = BARC(S=BARC_P, BI=[FAB_ID, 0x01, 0x02, 0x03, 0x04, 0x05])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    frame.show()
    # ls(frame)
    sendp(frame, iface=intf)
    print("\n\n")


def test_bpss(intf):
    """
    Test BARC proposal to spine switch
    """

    # make BARC frame
    ether = CEther(dst=xtos(BARC_DA), src=":".join(src_addr), type=TYPE_BARC)

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


captures = []


def listen(intf):
    """
    Listen for incoming packets
    """

    def show(x):
        print("Received frames:")
        x = deparser(x)
        x.show()
        # ls(x)
        print("\n\n")
        captures.append(x)

    # start asynchronous sniffer to log replies
    t = AsyncSniffer(prn=lambda x: show(x), store=False, iface=intf)

    t.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="test.py", description="Run host traffic simulation"
    )
    parser.add_argument("interface", type=str)
    args = parser.parse_args()

    # start async sniffing
    listen(args.interface)
    time.sleep(5)

    # send BARC initilization frame
    test_bi(args.interface)
    time.sleep(10)
