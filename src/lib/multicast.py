# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

def get_ports(b):
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

def add_rules(g2p, thrift_port, thrift_ip="127.0.0.1"):
    controller = SimpleSwitchThriftAPI(thrift_port=thrift_port, thrift_ip=thrift_ip)

    for grp, ports in list(g2p.items())[1:]:
        controller.mc_mgrp_create(grp)
        controller.mc_node_create(0, ports)
        controller.mc_node_associate(grp, grp-1)

def mcast_setup(K, net):
    # map group ids to ports
    g2p = dict(enumerate([get_ports(b) for b in range(2**K)]))

    for sname in net.ft_switches["rck"]:
        add_rules(g2p, net.net.get(sname).thrift_port)

    for sname in net.ft_switches["fab"]:
        add_rules(g2p, net.net.get(sname).thrift_port)

    for sname in net.ft_switches["spn"]:
        add_rules(g2p, net.net.get(sname).thrift_port)
    