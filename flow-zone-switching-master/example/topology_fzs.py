#!/usr/bin/env python2
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep
import subprocess
import os
import re

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--thrift-port',
                    help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--repeat', '-r',
                    help='Number of times to run test',
                    type=int, action="store", default=5)
args = parser.parse_args()

# Simple dataceenter topology formed by 1 spine (1 spine switch) and 2 pods (1 fabric switch, 1 rack switch, 1 host each pod)
class SingleSwitchTopo(Topo):
    "Single switch connected to 2 hosts."
    def __init__(self, sw_path, json_path, thrift_port, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        spine = self.addSwitch('s1',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port,
                                pcap_dump = False)
        fabric1 = self.addSwitch('s2',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port+1,
                                pcap_dump = False)
        fabric2 = self.addSwitch('s3',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port+2,
                                pcap_dump = False)
        rack1 = self.addSwitch('s4',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port+3,
                                pcap_dump = False)
        rack2 = self.addSwitch('s5',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port+4,
                                pcap_dump = False)
        host1 = self.addHost('h1',
                            ip = "10.0.0.11/24",
                            mac = '00:01:01:01:02:02')
        host2 = self.addHost('h2',
                            ip = "10.0.0.12/24",
                            mac = '00:02:01:01:02:02')
        self.addLink(host1, rack1)
        self.addLink(host2, rack2)
        self.addLink(rack1, fabric1)
        self.addLink(rack2, fabric2)
        self.addLink(fabric1, spine)
        self.addLink(fabric2, spine)

def start_iperf(net, client_name, server_name):
    h2 = net.getNodeByName(server_name)
    # print "Starting iperf server..."
    server = h2.popen("iperf -s")
    h1 = net.getNodeByName(client_name)
    # -f m: report in Mbits
    return h1.popen("iperf -f m -c %s -t 30" % (h2.IP()), stdout=subprocess.PIPE)

def configure_dp(commands_path, thrift_port):
    cmd = ["/home/admuc3m/P4/behavioral-model/tools/runtime_CLI.py", # bmv2 CLI path
           "--thrift-port", str(thrift_port)]
    with open(commands_path, "r") as f:
        print " ".join(cmd)
        sub_env = os.environ.copy()
        pythonpath = ""
        if "PYTHONPATH" in sub_env:
            pythonpath = sub_env["PYTHONPATH"] + ":"
        sub_env["PYTHONPATH"] = pythonpath + \
                                "/home/admuc3m/P4/behavioral-model/thrift_src/gen-py/" # bmv2 python path
        subprocess.Popen(cmd, stdin = f, env = sub_env).wait()

def run_measurement(net, client_name, server_name):
    iperf_proc = start_iperf(net, client_name, server_name)
    out, _ = iperf_proc.communicate()
    res = re.findall(r"(\d+) Mbits/sec", out)
    return res[-1]

def main():
    thrift_port = args.thrift_port
    num_hosts = 2

    sw_path = "/home/admuc3m/P4/behavioral-model/targets/simple_switch/simple_switch" # bmv2 simple switch path
    json_path = "./fzs.json" # p4 json file
    topo = SingleSwitchTopo(sw_path, json_path, thrift_port)
    net = Mininet(topo = topo, host = P4Host, switch = P4Switch,
                  controller = None)
    net.start()

    h1 = net.get('h1')
    h1.setARP("10.0.0.12", "00:02:01:01:02:02")
    h2 = net.get('h2')
    h2.setARP("10.0.0.11", "00:01:01:01:02:02")

    for n in xrange(num_hosts):
        h = net.get('h%d' % (n + 1))
        h.describe()

    sleep(1)

    configure_dp("./config/spine.config", thrift_port) # configuration file - spine
    configure_dp("./config/fabric1.config", thrift_port+1) # configuration file - fabric
    configure_dp("./config/fabric2.config", thrift_port+2) # configuration file - fabric
    configure_dp("./config/rack1.config", thrift_port+3) # configuration file - rack
    configure_dp("./config/rack2.config", thrift_port+4) # configuration file - rack

    sleep(1)

    print "Ready !"

    net.pingAll()

    throughputs = []
    for i in xrange(args.repeat):
        sleep(1)
        print "Running iperf measurement {} of {}".format(i + 1, args.repeat)
        t = run_measurement(net, "h1", "h2")
        print t, "Mbps"
        throughputs.append(t)
    throughputs.sort()
    print "Median throughput is", throughputs[args.repeat / 2], "Mbps"

    CLI( net )
    net.stop()
    # just in case...
    subprocess.Popen("pgrep -f iperf | xargs kill -9", shell=True).wait()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
