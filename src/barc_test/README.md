# BARC test

A simple BARC protocol test. There are 2 hosts connected to a single switch connected at port 0 and port 128 (the second host's port needs to be flipped). We first send one of the BARC frames from host A and listen at host B, and then do the opposite, making the hosts simulate either a host or switch in the topology. The switch just forwards the frames, making modifications according to the protocol.

## Usage

- Run `make` or `make run` to create the network.
- Run the following commands to start shell instances in the hosts;
    ```python
    mininet> xterm h1
    mininet> xterm h2
    ```
- Use the shells to start python in both hosts;
    ```
    python3 | tee output_h<host_number>.txt
    ```
- In host h2, run the following commands;
    ```python
    from test import *
    listen("h2")
    ```
- In host h1, run the following commands (press return after each frame is sent to get back the prompt);
    ```python
    from test import *
    test_bprs("h1")
    test_bpfs("h1")
    test_bpss("h1")
    test_bi("h1")
    ```
- Press return in h2 to see outputs.
- The outputs of the tests are also written to `output_h<host_number>.txt`.
- Run `make clean` to remove intermediate files.

## Notes

- Currently works with 8-bit port addressing. Need to figure out how to do 9-bit addressing.