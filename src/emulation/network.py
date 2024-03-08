# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.fattree import FatTreeTopo
from lib.multicast import setup_example, setup_mcast

K = 4
DROP_PORT = 511
CTRL_SESSION = CTRL_PORT = 510
with open("runtime.p4", "w") as f:
    f.write(
        f"""/*
 * This file is generated dynamically at runtime.
 * DO NOT MAKE EDITS HERE AS THEY WILL BE OVERWRITTEN.
 */


/* -*- P4_16 -*- */

const int TREE_K={bin(K)};
const int DROP_PORT = {bin(DROP_PORT)};
const bit<32> CTRL_SESSION = {bin(CTRL_SESSION)};"""
    )

# initialize network
net = FatTreeTopo(loglevel="info")

# build k-ary fat-tree
net.setup(src="switch.p4", k=K, ctrl_port=CTRL_PORT)

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
net.disableCli()
net.startNetwork()

# setup mcast groups and mirroring sessions
setup_mcast(K, net, CTRL_PORT)

# setup example entries mcast table
setup_example(K, net)

threads = []
for hname in net.ft_hosts:
    hobj = net.net.get(hname)
    hobj.cmd(f"nohup python3 test.py {hobj.intf().name} > outputs/output_{hname}.txt &")

# this timeout will need to be
# increased for larger k values
time.sleep(10)

# start the controller
ctrl = net.net.get(net.ctrl)
ctrl.cmd(f"nohup python3 ../lib/controller.py > outputs/output_ctrl.txt &")

net.start_net_cli()

net.net.stop()
