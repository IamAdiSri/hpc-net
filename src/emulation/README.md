# emulation

Emulates all protocols (BARC, CORE, Unicast, Multicast) on a K-ary FatTree.

## Usage

Run `make` to build and start the network; the following steps are performed in order:
1. Start Mininet
2. Create files needed at runtime
3. Initialize the FatTree
4. Start the network
5. Start the controllers
6. Initiate the BARC protocol for all devices to resolve their addresses
7. Set up two example Multicast groups
8. Launch the Mininet console

Once in the Mininet console, you can interact with the hosts by starting a host terminal using the command `xterm <host_name>`. You can send packets from the host in this terminal by starting a python shell and importing methods from the `../lib/host_ops.py` module.

Once you're done, run `make clean` to remove runtime files and logs. You can also run `make stop` if you just want to shut the network down but leave the logs intact.

## Logging

Switches, hosts and controllers all write their own logs in the following files:
- Host logs are written to `outputs/<host_name>.txt`. These will only occur during BARC resolution process.
- Controller logs are written to `outputs/<switch_name>.txt`.
- Switch logs are written to the `log` directory.
