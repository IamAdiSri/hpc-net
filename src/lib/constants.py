# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# frame types
TYPE_BARC = 0x22F0  # BARC frame 0b0010001011110000
TYPE_UNIC = 0x22F1  # Unicast frame 0b0010001011110001

# BARC constants
BARC_DA = 0x0180C2000000
BARC_I = 0xA
BARC_P = 0xB

# node identifiers
HST_ID = 0xA0  # Host identifier 0b10100000
SPN_ID = 0xE0  # Spine identifier 0b11100000
FAB_ID = 0xF0  # Fabric identifier 0b11110000
RCK_ID = 0xB0  # Rack identifier 0b10110000
