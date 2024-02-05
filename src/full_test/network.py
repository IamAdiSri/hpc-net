import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.fattree import FatTreeTopo

# initialize network
net = FatTreeTopo(loglevel="info")

# build k-ary fat-tree
K = 4
net.setup(src="switch.p4", k=K)
with open("runtime.p4", "w") as f:
    f.write(
f"""/*
 * This file is generated dynamically at runtime.
 * DO NOT MAKE EDITS HERE AS THEY WILL BE OVERWRITTEN.
 */


/* -*- P4_16 -*- */

const int TREE_K={bin(K)};"""
    )

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
net.disableCli()
net.startNetwork()

threads = []
for hname in net.ft_hosts:
    hobj = net.net.get(hname)
    hobj.cmd(f"nohup python3 test.py {hobj.intf().name} > outputs/output_{hname}.txt &")

# this timeout will need to be
# increased for larger k values
time.sleep(10)

net.start_net_cli()

net.net.stop()
