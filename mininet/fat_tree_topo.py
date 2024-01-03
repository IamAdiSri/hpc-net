from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class FatTreeTopo(Topo):
    def build(self, k=4):
        # k is the parameter that determines the size of the Fat-Tree

        # spine switches
        spine_switches = [self.addSwitch(f"spn{i}") for i in range((k//2)**2)]

        # |pods| = k

        # fabric switches
        fab_switches = [self.addSwitch(f"fab{i}") for i in range(k**2//2)]

        # tor switches
        tor_switches = [self.addSwitch(f"tor{i}") for i in range(k**2//2)]

        # servers
        servers = [self.addHost(f"srv{i}") for i in range(k**3//4)]

        # Connect spine switches to fabric switches
        for c in range((k//2)**2):
            for pod in range(k):
                f = pod * (k//2) + c//(k//2)
                self.addLink(spine_switches[c], fab_switches[f])

        # Connect fabric switches to tor switches
        for f in range((k**2)//2):
            si = f//(k//2) * (k//2)
            for t in range(si, si + k//2):
                self.addLink(fab_switches[f], tor_switches[t])

        # Connect tor switches to servers
        for t in range((k**2)//2):
            si = t * (k//2)
            for s in range(si, si + k//2):
                self.addLink(tor_switches[t], servers[s])

def run_fat_tree_topo():
    setLogLevel('info')

    k = 4  # You can adjust the parameter k to change the size of the Fat-Tree
    topo = FatTreeTopo(k=k)
    net = Mininet(topo=topo)
    net.start()

    # You can run your tests or commands here
    # Example: net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run_fat_tree_topo()


# ens32: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
#         inet 192.168.216.137  netmask 255.255.255.0  broadcast 192.168.216.255
#         inet6 fe80::20c:29ff:feb2:20e2  prefixlen 64  scopeid 0x20<link>
#         ether 00:0c:29:b2:20:e2  txqueuelen 1000  (Ethernet)
#         RX packets 57063  bytes 14529062 (14.5 MB)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 51258  bytes 7899259 (7.8 MB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0