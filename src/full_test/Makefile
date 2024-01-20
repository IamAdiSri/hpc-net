all: ../lib/constants.p4 ../lib/headers.p4 switch.p4 ../lib/fattree.py network.py test.py
	mkdir -p outputs
	sudo -E python3 network.py

clean:
	sudo mn -c
	sudo rm -rf log pcap __pycache__ outputs
	sudo rm switch.json switch.p4i
	sudo rm topology.json
	