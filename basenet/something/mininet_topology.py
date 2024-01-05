# define your network topology and integrate the P4 program
from mininet.net import Mininet
from nodes import P4Switch
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet()

    # Create P4-enabled switch using the simple.json compiled P4 program
    switch = net.addSwitch('s1', cls=P4Switch, filename='simple.json', thrift_port=9090)

    # Add hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    # Connect hosts to the switch
    net.addLink(h1, switch)
    net.addLink(h2, switch)

    net.start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()

#  run wtih: sudo python mininet_topology.py
# test connectivity: mininet> pingall
