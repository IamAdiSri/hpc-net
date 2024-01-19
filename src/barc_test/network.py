from p4utils.mininetlib.network_API import NetworkAPI

# initialize network
net = NetworkAPI()
net.setLogLevel("info")

# setup one switch and 2 hosts
s1 = net.addP4Switch("s1")
h1 = net.addHost("h1")  # low
h2 = net.addHost("h2")  # high

# deploy switch program
net.setP4Source("s1", "switch.p4")

# link the switches and the host
net.addLink("s1", "h1")
net.setIntfPort("s1", "h1", 0)  # Set the number of the port on s1 facing h1
net.setIntfPort("h1", "s1", 0)  # Set the number of the port on h1 facing s1


net.addLink("s1", "h2")
net.setIntfPort("s1", "h2", 256)
net.setIntfPort("h2", "s1", 0)

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
# net.disableCli()
net.startNetwork()
