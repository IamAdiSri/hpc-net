from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()
net.setLogLevel('info')

net.addP4Switch('s1')
net.addHost('h1')

net.setP4Source('s1', 'fzs.p4')

net.addLink('s1', 'h1')

net.setIntfPort('s1', 'h1', 1)  # Set the number of the port on s1 facing h1
net.setIntfPort('h1', 's1', 0)  # Set the number of the port on h1 facing s1

# net.setIntfIp('h1','s1','10.0.0.1/24') # The interface of h1 facing s1 has IP 10.0.0.1/24
# net.setIntfIp('h1','s1','00:00:00:00:00:01') # The interface of h1 facing s1 has MAC 00:00:00:00:00:01

net.enablePcapDumpAll()
net.enableLogAll()

net.enableCli()
net.startNetwork()