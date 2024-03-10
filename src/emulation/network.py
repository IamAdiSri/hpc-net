# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.fattree import FatTreeTopo
from lib.mc_examples import example_1

K = 4
DROP_PORT = 511
CTRL_SESSION = 510
CTRL_PORT = K

# generate runtime constants for p4
with open("runtime.p4", "w") as f:
    f.write(
        f"""/*
 * This file is generated dynamically at runtime.
 * DO NOT MAKE EDITS HERE AS THEY WILL BE OVERWRITTEN.
 */


/* -*- P4_16 -*- */

const int TREE_K={bin(K)}; // {K}
const int DROP_PORT = {bin(DROP_PORT)}; // {DROP_PORT}
const int CTRL_PORT = {bin(CTRL_PORT)}; // {CTRL_PORT}
const bit<32> CTRL_SESSION = {bin(CTRL_SESSION)}; // {CTRL_SESSION}
"""
    )

# initialize network
net = FatTreeTopo(
    k=K,
    p4src="switch.p4",
    drop_port=DROP_PORT,
    ctrl_port=CTRL_PORT,
    p4rt=True,
    loglevel="info",
)

# build k-ary fat-tree
net.setup()

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
net.disableCli()
net.startNetwork()

print("Starting controllers on all nodes...")
for stype in net.ft_switches:
    for sname in net.ft_switches[stype]:
        sobj = net.net.get(sname)
        sobj.cmd(
            f"nohup python3 -u ../lib/controller.py --k {K} --sname {sname} --ctr-session {CTRL_SESSION} > outputs/{sname}_c.txt &"
        )

# this timeout will need to be
# increased for larger k values
time.sleep(20)

# setup example entries mcast table
print("Setting up multicast example 1...")
# example_1(K, net)

# this timeout will need to be
# increased for larger k values
# time.sleep(20)

threads = []
for hname in net.ft_hosts:
    hobj = net.net.get(hname)
    hobj.cmd(
        f"nohup python3 -u run_barc.py {hobj.intf().name} > outputs/{hname}_s.txt &"
    )

# this timeout will need to be
# increased for larger k values
time.sleep(10)

net.start_net_cli()

net.net.stop()
