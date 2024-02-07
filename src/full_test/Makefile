all: ../lib/headers.p4 ../lib/constants.p4 ../lib/registers.p4 ../lib/parser.p4 ../lib/ingress.p4 ../lib/deparser.p4 switch.p4 ../lib/fattree.py network.py test.py
	mkdir -p outputs
	sudo -E python3 network.py

clean:
	sudo mn -c
	sudo rm -rf log pcap __pycache__ outputs
	sudo rm switch.json switch.p4i runtime.p4
	sudo rm topology.json
	rm preprocessed_logs.json
	