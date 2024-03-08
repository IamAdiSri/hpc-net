# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


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


def add_mcast_groups(g2p, thrift_port, thrift_ip="127.0.0.1"):
    """
    https://github.com/p4lang/behavioral-model/blob/main/docs/runtime_CLI.md
    https://nsg-ethz.github.io/p4-utils/p4utils.utils.thrift_API.html
    """
    controller = SimpleSwitchThriftAPI(thrift_port=thrift_port, thrift_ip=thrift_ip)

    for grp, ports in list(g2p.items())[1:]:
        controller.mc_mgrp_create(grp)
        # node handle is called l1 handle in logs
        node_handle = controller.mc_node_create(0, ports)
        controller.mc_node_associate(grp, node_handle)


def setup_mcast(K, net, ctrl_port=None):
    # map group ids to ports
    g2p = dict(enumerate([gen_mcast_ports(b) for b in range(2**K)]))

    # add mgroup for controller
    if ctrl_port:
        g2p[ctrl_port] = [ctrl_port]

    for sname in net.ft_switches["rck"]:
        add_mcast_groups(g2p, net.net.get(sname).thrift_port)

    for sname in net.ft_switches["fab"]:
        add_mcast_groups(g2p, net.net.get(sname).thrift_port)

    for sname in net.ft_switches["spn"]:
        add_mcast_groups(g2p, net.net.get(sname).thrift_port)


def add_table_entries(K, net, sname, ca, ports):
    thrift_ip = "127.0.0.1"

    ca = [f"0x{f}" for f in ca.split(":")]

    thrift_port = net.net.get(sname).thrift_port
    controller = SimpleSwitchThriftAPI(thrift_port=thrift_port, thrift_ip=thrift_ip)

    for ingressPort in range(K):
        i = K - ingressPort - 1
        if ports[i] == "1":
            new_ports = [b for b in ports]
            new_ports[i] = "0"
            controller.table_add(
                "SFZSIngress.mc_table",
                "SFZSIngress.multicast_to_group",
                ca + [str(ingressPort)],
                [f"0b{''.join(new_ports)}"],
            )
            controller.table_add(
                "SFZSIngress.placeholder_table",
                "SFZSIngress.placeholder_action",
                ca + [str(ingressPort)],
                [],
            )


def setup_example(K, net):
    # rack switches
    add_table_entries(K, net, "rck_1_1", "BF:01:00:00:00:01", "0110")
    add_table_entries(K, net, "rck_2_0", "BF:01:00:00:00:01", "0101")
    add_table_entries(K, net, "rck_2_1", "BF:01:00:00:00:01", "0110")
    add_table_entries(K, net, "rck_3_1", "BF:01:00:00:00:01", "0111")

    # fabric switches
    add_table_entries(K, net, "fab_1_0", "BF:01:00:00:00:01", "1010")
    add_table_entries(K, net, "fab_2_0", "BF:01:00:00:00:01", "1011")
    add_table_entries(K, net, "fab_3_0", "BF:01:00:00:00:01", "1010")

    # spine switches
    add_table_entries(K, net, "spn_1_0", "BF:01:00:00:00:01", "1110")
