# Echo Test

A simple echo test between a single host and switch pair, where the host sends a BARC frame to the P4 switch. The switch then makes a few modifications the frame (including changing it into a Unicast frame) and sends it back to the host.

## Usage

- Run `make` or `make run` to create the network and run the echo test.
- The output of the test is written to `output.txt`.
- Run `make clean` to remove intermediate files.