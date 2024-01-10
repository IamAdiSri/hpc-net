#! /usr/bin/python3

import argparse
import pickle
from scapy.all import *
from scapy.layers.l2 import *

from lib.headers import CEther, BARC, deparser
from lib.constants import *
from lib.utils import *

def barc_init(hname):
    ether = CEther(
        dst=xtos(BARC_DA), 
        type=TYPE_BARC
    )

    barc = BARC(
        S=BARC_I,
        BI=[HST_ID, 0x00, 0x00, 0x00, 0x00, 0x00]
    )

    frame = ether/barc
    # ls(frame)
    

    captures = []
    t = AsyncSniffer(
        prn=lambda x: captures.append(x), 
        store=False,
        iface=f"{hname}-eth0"
    )

    t.start()
    time.sleep(0.1)
    
    sendp(frame, iface=f"{hname}-eth0")
    
    time.sleep(0.1)
    t.stop()

    for pkt in captures:
        ls(pkt)

    return captures


if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog='run_sim.py',
                    description='Run host traffic simulation')
    parser.add_argument("hostname", type=str)
    args = parser.parse_args()

    caps = barc_init(args.hostname)
    
    with open('caps', 'wb') as f:
        pickle.dump(caps, f, pickle.HIGHEST_PROTOCOL)
    
    print("Simulation completed")