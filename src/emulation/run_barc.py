# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import argparse
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], ".."))

from lib.host_ops import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="run_barc.py", description="Run BARC protocol"
    )
    parser.add_argument("interface", type=str)
    args = parser.parse_args()

    # start async sniffing
    listen(args.interface)

    # this timeout will need to be
    # increased for larger k values
    time.sleep(1)

    # send BARC initilization frame
    test_bi(args.interface)

    # this timeout will need to be
    # increased for larger k values
    time.sleep(1)
