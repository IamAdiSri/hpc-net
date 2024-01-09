# Create a simple controller script (e.g., simple_controller.py) using the P4Runtime Python API to send and receive P4 Runtime messages

from p4utils.utils.topology import Topology
from p4utils.simple_controller import SimpleController

class MyController(SimpleController):
    def __init__(self, sw_name, json_path, topo):
        super(MyController, self).__init__(sw_name, json_path, topo)

    def packet_in_handler(self, pkt):
        # Handle packet-in events
        print("Received Packet-In Event:")
        print(pkt)

if __name__ == '__main__':
    # Create a Topology instance
    topo = Topology(db=topology_db)

    # Specify the switch name and path to the compiled JSON
    switch_name = "s1"
    json_path = "simple.json"

    # Instantiate and run the controller
    controller = MyController(switch_name, json_path, topo)
    controller.start()

#  run with: python3 simple_controller.py
