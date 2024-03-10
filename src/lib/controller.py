# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import argparse
import os
import sys

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from scapy.all import sniff

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.constants import *
from lib.headers import deparser
from lib.utils import capture_stdout


class Controller:
    """
    Local controller for P4 switch
    """

    def __init__(self, k, sname, ctr_session, topo="topology.json"):
        """
        Initialize controller start setup

        Args:
            k: Size of K-ary FatTree
            sname: Name of local switch
            ctr_session: Mirror ID for cloning to controller
            topo: Topology file for mininet FatTree

        References:
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

        print(sname, self.thrift_port)
        self.init()

    def init(self):
        """
        Setup default switch tables
        """

        self.controller.reset_state()
        self.add_mcf_groups()
        print("Added multicast forwarding groups")
        self.add_ctr_mirror()
        print("Added mirror for control session")

    def add_mcf_groups(self):
        """
        Add Multicast forwarding groups
        """

        def gen_mcast_ports(b):
            """
            Generate list of ports from bitmask
            """

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
            Add Multicast groups

            Args:
                g2p: Mapping of Group ID to member ports

            References:
                https://github.com/p4lang/behavioral-model/blob/main/docs/runtime_CLI.md
                https://nsg-ethz.github.io/p4-utils/p4utils.utils.thrift_API.html
            """

            for grp, ports in list(g2p.items())[1:]:
                self.controller.mc_mgrp_create(grp)
                # node handle is called l1 handle in logs
                node_handle = self.controller.mc_node_create(0, ports)
                self.controller.mc_node_associate(grp, node_handle)

        # map group ids to ports
        g2p = dict(enumerate([gen_mcast_ports(b) for b in range(2**self.k)]))

        add_mcast_groups(g2p)

    def add_ctr_mirror(self):
        """
        Add mirror session for cloning packets to controller
        """

        self.controller.mirroring_add(self.ctr_session, self.cpu_port)

    def core_handler(self, ca, inport):
        """
        Add/Update rules on receiving a CORE packet

        Args:
            ca: Collective address
            inport: IngressPort on which
                    the packet was received at switch
        """
        ca = [hex(f) for f in ca]

        print(">>>")
        self.controller.table_dump("SFZSIngress.mc_table")
        print(">>>")

        @capture_stdout
        def get_entry(key):
            self.controller.table_dump_entry_from_key("SFZSIngress.mc_table", key)

        # get entry if key already exists
        entry = get_entry(ca + [hex(inport)])
        print(entry)

        old_ports = 0

        # do nothing if key already exists
        if entry != "Invalid table operation (BAD_MATCH_KEY)\n":
            print("core_handler: Key already exists in table")
            return

        # check if any other ports are linked to this CA
        new_members = {
            inport,
        }
        old_members = set()
        for p in range(self.k):
            if p != inport:
                key = ca + [hex(p)]
                entry = get_entry(key)
                print(key, entry)

                if entry != "Invalid table operation (BAD_MATCH_KEY)\n":
                    # add port to members
                    old_members.add(p)

                    # identify all other member ports from match
                    old_ports = entry.split("\n")[-2].split(" - ")[-1]
                    old_ports = int(old_ports, 16)

                    p = 0
                    while old_ports != 0:
                        if old_ports & 1 == 1:
                            old_members.add(p)
                        old_ports >>= 1
                        p += 1

                    # break out of loop
                    break

        # add the egress port to the member list
        if self.sname[0] == "r":  # rack switch
            outport = int(ca[2], 16) + self.k // 2
            if outport not in old_members:
                new_members.add(outport)
        elif self.sname[0] == "f":  # fabric switch
            outport = int(ca[1], 16) + self.k // 2
            if outport not in old_members:
                new_members.add(outport)

        # convert members to bit mask
        bitmask = ["0" for _ in range(self.k)]
        for m in new_members:
            bitmask[self.k - 1 - m] = "1"
        for m in old_members:
            bitmask[self.k - 1 - m] = "1"

        print(f"Member bitmask: {bitmask}\n")

        # update the rules for all members
        for i in range(self.k):
            if bitmask[self.k - 1 - i] == "1":
                i_mask = [b for b in bitmask]
                i_mask[self.k - 1 - i] = "0"
                i_mask = f"0b{''.join(i_mask)}"

                key = ca + [hex(i)]
                print(key)

                if i in new_members:
                    self.controller.table_add(
                        "SFZSIngress.mc_table",
                        "SFZSIngress.multicast_to_group",
                        key,
                        [i_mask],
                    )
                    self.controller.table_add(
                        "SFZSIngress.placeholder_table",
                        "SFZSIngress.placeholder_action",
                        key,
                        [],
                    )
                elif i in old_members:
                    self.controller.table_modify_match(
                        "SFZSIngress.mc_table",
                        "SFZSIngress.multicast_to_group",
                        key,
                        [i_mask],
                    )
                    self.controller.table_modify_match(
                        "SFZSIngress.placeholder_table",
                        "SFZSIngress.placeholder_action",
                        key,
                        [],
                    )

    def process(self, pkt):
        """
        Process received pkt

        Args:
            pkt: packet received
        """
        pkt = deparser(pkt)
        pkt.show()

        if int("".join(pkt.dst.split(":")), 16) == NCB_DA and pkt.type == TYPE_CORE:
            self.core_handler(pkt.CA, pkt.inport)

    def start(self):
        """
        Start listening loop
        """
        cpu_port_intf = str(self.topo.get_cpu_port_intf(self.sname))
        sniff(iface=cpu_port_intf, prn=self.process)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="controller.py", description="Run controller")
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--sname", type=str, required=True)
    parser.add_argument("--ctr-session", type=str, required=True)
    parser.add_argument("--topo", type=str, default="topology.json")
    args = parser.parse_args()

    controller = Controller(args.k, args.sname, args.ctr_session, args.topo)
    controller.start()
