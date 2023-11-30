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

        # Connect core switches to aggregation switches
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
