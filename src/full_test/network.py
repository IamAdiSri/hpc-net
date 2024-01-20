import os
import sys

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.fattree import FatTreeTopo

# initialize network
net = FatTreeTopo(loglevel="info")

# build k-ary fat-tree
net.setup(src="switch.p4", k=4)

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
# net.disableCli()
net.startNetwork()
