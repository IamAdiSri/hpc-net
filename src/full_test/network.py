# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.fattree import FatTreeTopo
from lib.multicast import mcast_setup

# initialize network
net = FatTreeTopo(loglevel="info")

# build k-ary fat-tree
K = 4
with open("runtime.p4", "w") as f:
    f.write(
        f"""/*
 * This file is generated dynamically at runtime.
 * DO NOT MAKE EDITS HERE AS THEY WILL BE OVERWRITTEN.
 */


/* -*- P4_16 -*- */

const int TREE_K={bin(K)};"""
    )
net.setup(src="switch.p4", k=K)

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
net.disableCli()
net.startNetwork()

# setup static rules in mcast table
mcast_setup(K, net)

threads = []
for hname in net.ft_hosts:
    hobj = net.net.get(hname)
    hobj.cmd(f"nohup python3 test.py {hobj.intf().name} > outputs/output_{hname}.txt &")

# this timeout will need to be
# increased for larger k values
time.sleep(10)

net.start_net_cli()

net.net.stop()
