from topology import BasicTopo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

def run_basic_topo():
    setLogLevel('info')

    topo = BasicTopo()
    net = Mininet(topo=topo)
    net.start()

    # You can run your tests or commands here
    # Example: net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run_basic_topo()