all: echo.p4 ../lib/constants.p4 ../lib/headers.p4 network.py run_test.py
	sudo python3 network.py

clean:
	sudo mn -c
	sudo rm -rf log pcap
	sudo rm echo.json echo.p4i
	sudo rm topology.json
	sudo rm output.txt