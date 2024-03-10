import os
import sys
import json
import argparse

import psutil
from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from scapy.all import sniff, AsyncSniffer

sys.path.append(os.path.join(sys.path[0], ".."))
from lib.headers import deparser
from lib.constants import *
from lib.utils import capture_stdout



class Controller:
    def __init__(self, k, sname, ctr_session, topo="topology.json"):
        """
        https://github.com/nsg-ethz/p4-learning/blob/master/exercises/04-L2_Learning/thrift/solution/l2_learning_controller.py
        """
        self.k = k
        self.sname = sname
        self.ctr_session = ctr_session
        self.topo = load_topo(topo)
        self.thrift_ip = self.topo.get_thrift_ip(sname)
        self.thrift_port = self.topo.get_thrift_port(sname)
        self.cpu_port = self.topo.get_cpu_port_index(sname)
        self.controller = SimpleSwitchThriftAPI(self.thrift_port, self.thrift_ip)

        self.init()

    def init(self):
        self.controller.reset_state()
        self.add_mcf_groups()
        print("Added multicast forwarding groups")
        self.add_ctr_mirror()
        print("Added mirror for control session")

    def add_mcf_groups(self):
        def gen_mcast_ports(b):
            curr = 0
            ports = []
            while b != 0:
                # check least significant bit
                if b & 1:
                    ports.append(curr)
                # right shift by 1
                b >>= 1
                curr += 1
            return ports
    
        def add_mcast_groups(g2p):
            """
            https://github.com/p4lang/behavioral-model/blob/main/docs/runtime_CLI.md
            https://nsg-ethz.github.io/p4-utils/p4utils.utils.thrift_API.html
            """

            for grp, ports in list(g2p.items())[1:]:
                self.controller.mc_mgrp_create(grp)
                # node handle is called l1 handle in logs
                node_handle = self.controller.mc_node_create(0, ports)
                self.controller.mc_node_associate(grp, node_handle)

        # map group ids to ports
        g2p = dict(enumerate(
            [gen_mcast_ports(b) for b in range(2**self.k)]
        ))

        add_mcast_groups(g2p)

    def add_ctr_mirror(self):
        self.controller.mirroring_add(self.ctr_session, self.cpu_port)

    def core_handler(self, ca, inport):
        ca = [hex(f) for f in ca]

        @capture_stdout
        def get_entry(key):
            self.controller.table_dump_entry_from_key(
            "SFZSIngress.mc_table",
            key
        )
        
        # get entry if key already exists
        entry = get_entry(ca + [str(inport)])
        print(entry)

        old_ports = 0

        # do nothing if key already exists
        if entry != 'Invalid table operation (BAD_MATCH_KEY)\n':
            print("core_handler: [ERROR] Key already exists in table; this packet should not have arrived at the controller")
            return
        
        # check if any other ports are 
        # also linked to this CA and 
        # delete their rules if so
        members = {inport,}
        for p in range(self.k):
            if p != inport:
                key = ca + [str(p)]
                entry = get_entry(key)
                print(entry)

                if entry != 'Invalid table operation (BAD_MATCH_KEY)\n':
                    # add port to members
                    members.add(p)

                    # identify all other member ports from match
                    old_ports = entry.split('\n')[-2].split(' - ')[-1]
                    if old_ports[0] == '0':
                        old_ports = int(old_ports[1])
                    else:
                        old_ports = int(old_ports)
                    
                    p = 0
                    while old_ports != 0:
                        if old_ports & 1 == 1:
                            members.add(p)
                        old_ports >>= 1
                        p += 1
                    
                    # delete table entries for all other members
                    for m in members:
                        if m != inport:
                            key = ca + [str(m)]
                            self.controller.table_delete_match(
                                "SFZSIngress.mc_table",
                                key,
                            )
                            self.controller.table_delete_match(
                                "SFZSIngress.placeholder_table",
                                key,
                            )

                    # break out of loop
                    break
        
        # add the egress port to the member list
        if self.sname[0] == 'r': # rack switch
            outport = int(ca[2], 16) + self.k//2
            members.add(outport)
        elif self.sname[0] == 'f': # fabric switch
            outport = int(ca[1], 16) + self.k//2
            members.add(outport)

        # convert members to bit mask
        bitmask = ['0' for _ in range(self.k)]
        for m in members:
            bitmask[self.k - 1 - m] = '1'

        print(f"Port bitmask: {bitmask}\n")

        # add back the rules for all members
        for i in range(self.k):
            if bitmask[self.k - 1 - i] == '1':
                i_mask = [b for b in bitmask]
                i_mask[self.k - 1 - i] = '0'
                i_mask = f"0b{''.join(i_mask)}"
                
                self.controller.table_add(
                    "SFZSIngress.mc_table",
                    "SFZSIngress.multicast_to_group",
                    ca + [str(i)],
                    [i_mask],
                )
                self.controller.table_add(
                    "SFZSIngress.placeholder_table",
                    "SFZSIngress.placeholder_action",
                    ca + [str(i)],
                    [],
                )

    def process(self, pkt):
        pkt = deparser(pkt)
        pkt.show()
        
        if int(''.join(pkt.dst.split(':')), 16) == NCB_DA and pkt.type == TYPE_CORE:
            self.core_handler(pkt.CA, pkt.inport)
        

    def start(self):
        cpu_port_intf = str(self.topo.get_cpu_port_intf(self.sname))
        sniff(iface=cpu_port_intf, prn=self.process)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="controller.py", description="Run controller"
    )
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--sname", type=str, required=True)
    parser.add_argument("--ctr-session", type=str, required=True )
    parser.add_argument("--topo", type=str, default="topology.json")
    args = parser.parse_args()

    # with open('outputs/output_ctrl.txt', 'w') as sys.stdout:
    controller = Controller(args.k, args.sname, args.ctr_session, args.topo)
    controller.start()
