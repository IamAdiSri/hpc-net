import pickle

with open('caps', 'rb') as f:
    caps = pickle.load(f)

pkt = caps[1]
pkt.show()

raw_pkt = bytes(pkt)
print(raw_pkt)

from lib.headers import CEther, BARC, UNIC
from lib.constants import *
from scapy.all import *
from scapy.layers.l2 import *

CEther(raw_pkt).show()
