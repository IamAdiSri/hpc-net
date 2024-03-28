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
parsed = {}
for switch_name in logs:
    parsed[switch_name] = []
    for i, line in enumerate(logs[switch_name]):
        line = line.strip()

        if "Processing packet received on port" in line:
            line = line.split(' ')
            parsed[switch_name].append({
                "ingress_time": convert_time(line[0][1:-1]),
                "ingress_port": int(line[-1]),
                "egress_times": [],
                "egress_ports": [],
                "type": None,
                "srcAddr": None,
                "dstAddr": None
            })

        elif "] Source Address: " in line:
            line = line.split(' ')
            parsed[switch_name][-1]["srcAddr"] = line[-1]

        elif "] Multicast DA: " in line:
            line = line.split(' ')
            parsed[switch_name][-1]["type"] = "Multicast"
            parsed[switch_name][-1]["dstAddr"] = line[-1]

        elif "] Unicast DA: " in line:
            line = line.split(' ')
            parsed[switch_name][-1]["type"] = "Unicast"
            parsed[switch_name][-1]["dstAddr"] = line[-1]

        elif "] BARC DA: " in line:
            line = line.split(' ')
            parsed[switch_name][-1]["type"] = "BARC"
            parsed[switch_name][-1]["dstAddr"] = line[-1]

        elif "] CoRe CA: " in line:
            line = line.split(' ')
            parsed[switch_name][-1]["type"] = "CORE"
            parsed[switch_name][-1]["dstAddr"] = line[-1]

        elif "Transmitting packet of size" in line or "] Egress port is " in line:
            line = line.split(' ')
            egress_time = convert_time(line[0][1:-1])
            egress_port = int(line[-1])
            if egress_port not in parsed[switch_name][-1]["egress_ports"]:
                parsed[switch_name][-1]["egress_times"].append(egress_time)
                parsed[switch_name][-1]["egress_ports"].append(egress_port)

    # remove dropped packets
    parsed[switch_name] = [p for p in parsed[switch_name] if p["egress_ports"] and p["egress_ports"][0] != 511]

with open(os.path.join(sys.path[0], "preprocessed_logs.json"), "w") as f:
    f.write(json.dumps(parsed, indent=2))
