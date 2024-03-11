# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


def run_example(hosts, ca, net):
    for hname in hosts:
        hobj = net.net.get(hname)
        hobj.cmd(
            f"cd ../lib/; nohup python3 -c 'from host_ops import test_core; test_core(\"{ca}\")' >> ../emulation/outputs/{hname}_s.txt &"
        )


def example_1(net):
    run_example(
        ["h_1_1_1", "h_2_0_0", "h_2_1_1", "h_3_1_0", "h_3_1_1"],
        "bf:01:00:00:00:01",
        net,
    )


def example_2(net):
    run_example(
        ["h_0_0_1", "h_1_0_0", "h_1_1_0", "h_1_1_1", "h_3_0_0"],
        "bf:01:01:00:00:01",
        net,
    )
