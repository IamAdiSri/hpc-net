all: ../lib/constants.p4 ../lib/constants.py ../lib/controller.py ../lib/deparser.p4 ../lib/egress.p4 ../lib/fattree.py ../lib/headers.p4 ../lib/headers.py ../lib/host_ops.py ../lib/ingress.p4 ../lib/mc_examples.py ../lib/parser.p4 ../lib/registers.p4 ../lib/utils.py network.py run_barc.py switch.p4
	mkdir -p outputs
	sudo -E python3 network.py

stop:
	sudo mn -c

clean: stop
	sudo rm -rf log pcap outputs
	sudo rm -f switch.json switch.p4i runtime.p4
	sudo rm -f topology.json switch_p4rt.txt
	sudo rm -rf __pycache__ ../lib/__pycache__
