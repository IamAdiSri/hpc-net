# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


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


def example_1(K, net):
    # rack switches
    add_table_entries(K, net, "r_1_1", "BF:01:00:00:00:01", "0110")
    add_table_entries(K, net, "r_2_0", "BF:01:00:00:00:01", "0101")
    add_table_entries(K, net, "r_2_1", "BF:01:00:00:00:01", "0110")
    add_table_entries(K, net, "r_3_1", "BF:01:00:00:00:01", "0111")

    # fabric switches
    add_table_entries(K, net, "f_1_0", "BF:01:00:00:00:01", "1010")
    add_table_entries(K, net, "f_2_0", "BF:01:00:00:00:01", "1011")
    add_table_entries(K, net, "f_3_0", "BF:01:00:00:00:01", "1010")

    # spine switches
    add_table_entries(K, net, "s_1_0", "BF:01:00:00:00:01", "1110")
