all: fzs.p4 constants.p4 headers.p4 network.py
	sudo python3 network.py

clean:
	sudo mn -c
	sudo rm -rf __pycache__
	sudo rm -rf lib/__pycache__
	sudo rm -rf log pcap
	sudo rm fzs.json fzs.p4i
	sudo rm topology.json