import networkx as nx 
import matplotlib.pyplot as plt 
   
  
# Defining a Class 
class GraphVisualization: 
   
    def __init__(self, k): 
          
        # visual is a list which stores all  
        # the set of edges that constitutes a 
        # graph 
        self.core_switches = ['spn{}'.format(i+1) for i in range(k**2//4)]
        self.agg_switches = ['fab{}'.format(i+1) for i in range(k**2//2)]
        self.edge_switches = ['tor{}'.format(i+1) for i in range(k**2//2)]
        self.hosts = ['srv{}'.format(i+1) for i in range(k**3//4)]

        n = (k**2//4) + 2*(k**2//2)

        self.visual = [] 
          
    # addEdge function inputs the vertices of an 
    # edge and appends it to the visual list 
    def addEdge(self, a, b): 
        temp = [a, b] 
        self.visual.append(temp) 
          
    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 

        G = nx.Graph()
        G.add_edges_from(self.visual)
        plt.figure(figsize=(12, 12))
        # pos = nx.spring_layout(G, k=0.15, iterations=20)
        # nx.draw_networkx(G, pos, ax = None, with_labels = True,font_size = 8, node_size = 250, node_color = 'lightgreen')
        nx.draw_networkx(G)
        plt.savefig('network.png')

# Driver code 
k = 6
G = GraphVisualization(k = k)

# Connect core switches to aggregation switches
for c in range((k//2)**2):
    for pod in range(k):
        f = pod * (k//2) + c//(k//2)
        # self.addLink(spine_switches[c], fab_switches[f])
        G.addEdge(G.core_switches[c], G.agg_switches[f])

# Connect fabric switches to tor switches
for f in range((k**2)//2):
    si = f//(k//2) * (k//2)
    for t in range(si, si + k//2):
        # self.addLink(fab_switches[f], tor_switches[t])
        G.addEdge(G.agg_switches[f], G.edge_switches[t])

# Connect tor switches to servers
for t in range((k**2)//2):
    si = t * (k//2)
    for s in range(si, si + k//2):
        # self.addLink(tor_switches[t], servers[s])
        G.addEdge(G.edge_switches[t], G.hosts[s])

G.visualize() 