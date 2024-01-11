from p4utils.mininetlib.network_API import NetworkAPI

# initialize network
net = NetworkAPI()
net.setLogLevel("info")

# setup one switch and one host
s1 = net.addP4Switch("s1")
h1 = net.addHost("h1")

# deploy switch program
net.setP4Source("s1", "switch.p4")

# link the switch and the host
net.addLink("s1", "h1")

# enable logging
net.enablePcapDumpAll()
net.enableLogAll()

# disable CLI and start network
net.disableCli()
net.startNetwork()

# get host and switch objects and execute
# test script within host
h1, s1 = net.net.get("h1", "s1")
h1.cmd('python3 run_test.py "h1" > output.txt')

net.stopNetwork()
print("Simulation completed. Output can be found in output.txt")
