# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import sys
import json
import datetime


def convert_time(timestamp):
    h, m, s = timestamp.split(":")
    s, ms = s.split(".")
    # choosing a random year, month and day
    # because it doesn't make a difference
    # as long as we don't cross midnight
    # while running the network
    return datetime.datetime(2012, 12, 12, int(h), int(m), int(s), int(ms)).timestamp()


logs = {}
logdir = os.path.join(sys.path[0], "log")

for filename in os.listdir(logdir):
    with open(os.path.join(logdir, filename), "r") as f:
        logs[filename.split(".")[1]] = f.readlines()

# remove unnecessary lines
for switch_name in logs:
    retained = []
    for i, line in enumerate(logs[switch_name]):
        line = line.strip()
        if "Processing packet received on port" in line:
            retained.append(line)
        elif "hdr.ethernet.etherType == TYPE_BARC" in line:
            retained.append(line)
        elif "] Source Address: " in line:
            retained.append(line)
        elif "] Destination Address: " in line:
            retained.append(line)
        elif "Egress port is" in line:
            retained.append(line)
    logs[switch_name] = retained

for l in logs["rck_0_0"]:
    print(l)

# make list of tuples
for switch_name in logs:
    formatted = []
    l = len(logs[switch_name])
    for i in range(0, l, 5):
        ingress_line = logs[switch_name][i]
        type_line = logs[switch_name][i + 1]
        sa_line = logs[switch_name][i+2]
        da_line = logs[switch_name][i+3]
        egress_line = logs[switch_name][i + 4]

        ingress_line = ingress_line.split(" ")
        type_line = type_line.split(" ")
        sa_line = sa_line.split(" ")
        da_line = da_line.split(" ")
        egress_line = egress_line.split(" ")
        t = {
            "ingress_time": convert_time(ingress_line[0][1:-1]),
            "ingress_port": int(ingress_line[-1]),
            "egress_time": convert_time(egress_line[0][1:-1]),
            "egress_port": int(egress_line[-1]),
            "type": "BARC" if type_line[-1] == "true" else "Payload",
            "srcAddr": sa_line[-1],
            "dstAddr": da_line[-1]
        }
        if t["egress_port"] != 511:
            formatted.append(t)
    logs[switch_name] = formatted

with open(os.path.join(sys.path[0], "preprocessed_logs.json"), "w") as f:
    f.write(json.dumps(logs, indent=2))
