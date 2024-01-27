all: ../lib/headers.p4 ../lib/constants.p4 ../lib/registers.p4 ../parser.p4 ../lib/ingress.p4 ../lib/deparser.p4 switch.p4 network.py test.py
	sudo -E python3 network.py

clean:
	sudo mn -c
	sudo rm -rf log pcap __pycache__
	sudo rm switch.json switch.p4i
	sudo rm topology.json
	sudo rm output*.txt