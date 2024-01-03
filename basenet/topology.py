from mininet.topo import Topo

class BasicTopo(Topo):
    def build(self):
        self.addHost("srv0")
        self.addHost("srv1")

        self.addSwitch("tor0")

        self.addLink("srv0", "tor0")
        self.addLink("tor0", "srv1")
