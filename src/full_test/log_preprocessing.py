import os
import sys
import json

logs = {}
logdir = os.path.join(sys.path[0], "log")

for filename in os.listdir(logdir):
    with open(os.path.join(logdir, filename), "r") as f:
        logs[filename.split('.')[1]] = f.readlines()

# remove unnecessary lines
for switch_name in logs:
    retained = []
    for i, line in enumerate(logs[switch_name]):
        line = line.strip()
        if "Processing packet received on port" in line:
            retained.append(line)
        elif "hdr.ethernet.etherType == TYPE_BARC" in line:
            retained.append(line)
        elif "Egress port is" in line:
            retained.append(line)
    logs[switch_name] = retained

# make list of tuples
for switch_name in logs:
    formatted = []
    l = len(logs[switch_name])
    for i in range(0, l, 3):
        ingress_line = logs[switch_name][i]
        type_line = logs[switch_name][i+1]
        egress_line = logs[switch_name][i+2]

        ingress_line = ingress_line.split(' ')
        type_line = type_line.split(' ')
        egress_line = egress_line.split(' ')
        t = {
            "ingress_time": ingress_line[0][1:-1],
            "ingress_port": int(ingress_line[-1]),
            "egress_time" : egress_line[0][1:-1],
            "egress_port" : int(egress_line[-1]),
            "type": "BARC" if type_line[-1] == "true" else "Payload"
        }
        if t["egress_port"] != 511:
            formatted.append(t)
    logs[switch_name] = formatted

with open(os.path.join(sys.path[0], "preprocessed_logs.json"), "w") as f:
    f.write(json.dumps(logs, indent=2))
