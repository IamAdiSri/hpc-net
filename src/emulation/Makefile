all: ../lib/headers.p4 ../lib/constants.p4 ../lib/registers.p4 ../lib/parser.p4 ../lib/ingress.p4 ../lib/deparser.p4 switch.p4 ../lib/fattree.py network.py test.py
	mkdir -p outputs
	sudo -E python3 network.py

stop:
	sudo mn -c

clean: stop
	sudo rm -rf log pcap outputs
	sudo rm -f switch.json switch.p4i runtime.p4
	sudo rm -f topology.json
	sudo rm -rf __pycache__ ../lib/__pycache__
	rm -f preprocessed_logs.json
	