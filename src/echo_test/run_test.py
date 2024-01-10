#! /usr/bin/python3

import argparse
import os
import sys

from scapy.all import *
from scapy.layers.l2 import *

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.constants import *
from lib.headers import BARC, CEther, deparser
from lib.utils import *


def barc_init(hname):
    # make CEther frame with dest MAC set to
    # special BARC address and etherType also
    # set to BARC identifier
    ether = CEther(dst=xtos(BARC_DA), type=TYPE_BARC)

    # make BARC inquiry frame with the first
    # field in BI set to host identifier
    barc = BARC(S=BARC_I, BI=[HST_ID, 0x00, 0x00, 0x00, 0x00, 0x00])

    # compile and display complete frame
    frame = ether / barc
    print("\nSending CEther/BARC frame:")
    ls(frame)
    print("\n\n")

    # start asynchronous sniffer to log replies
    captures = []
    t = AsyncSniffer(
        prn=lambda x: captures.append(x), store=False, iface=f"{hname}-eth0"
    )
    t.start()

    # wait for a bit and send frame
    time.sleep(0.1)
    sendp(frame, iface=f"{hname}-eth0")

    # wait for a bit and stop sniffer
    time.sleep(0.1)
    t.stop()

    return captures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="run_sim.py", description="Run host traffic simulation"
    )
    parser.add_argument("hostname", type=str)
    args = parser.parse_args()

    # send BARC initilization frame
    captures = barc_init(args.hostname)

    # receive and display modified UNIC frame
    print("Received CEther/UNIC frames from switch:")
    pkt = deparser(captures[1])
    ls(pkt)
