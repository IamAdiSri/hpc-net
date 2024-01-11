/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


// frame types
const bit<16> TYPE_BARC = 0x22F0; // BARC frame 0b0010001011110000
const bit<16> TYPE_UNIC = 0x22F1; // Unicast frame 0b0010001011110001

// BARC constants
const addr_t BARC_DA = {
    f0 = 0x01,
    f1 = 0x80,
    f2 = 0xC2,
    f3 = 0x00,
    f4 = 0x00,
    f5 = 0x00
};
const bit<4>  BARC_I  = 0xA;
const bit<4>  BARC_P  = 0xB;

// node identifiers
const bit<8> HST_ID = 0xAE; // Host identifier 0b10101110
const bit<8> SPN_ID = 0xEE; // Spine identifier 0b11101110
const bit<8> FAB_ID = 0xFE; // Fabric identifier 0b11111110
const bit<8> RCK_ID = 0xBE; // Rack identifier 0b10111110