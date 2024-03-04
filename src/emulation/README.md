# emulation

Emulates all protocols on a FatTree.

## Usage

- Run `make` to build and start the network, and then run the BARC protocol.
- Once the BARC protocol completes, you will enter the mininet CLI.
- You can start a host terminal using the command `xterm <host_name>`. You can run tests in this terminal by starting a python shell and importing methods from the `test.py` module.
- Host logs are written to the `outputs` directory.
- Switch logs are written to the `log` directory.
- Run `make clean` to remove runtime files.
