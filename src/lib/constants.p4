/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


/* -*- P4_16 -*- */

// frame etherTypes
const bit<16> TYPE_BARC = 0x22F0; // BARC frame 0b0010001011110000
const bit<16> TYPE_CORE = 0x88B6; // CORE frame 0b1000100010110110

// Nearest Customer Bridge (NCB) address
const addr_t NCB_DA = {
    f0 = 0x01,
    f1 = 0x80,
    f2 = 0xC2,
    f3 = 0x00,
    f4 = 0x00,
    f5 = 0x00
};

// BARC subtypes
const bit<4>  BARC_I  = 0xA;
const bit<4>  BARC_P  = 0xB;

// CORE subtypes
const bit<16> CORE_S = 0x0000;

// node identifiers
const bit<8> SPN_ID = 0xBE; // Spine identifier 0b10111110
const bit<8> FAB_ID = 0xFE; // Fabric identifier 0b11111110
const bit<8> RCK_ID = 0xEE; // Rack identifier 0b11101110
const bit<8> HST_ID = 0xAE; // Host identifier 0b10101110

// packet instance type constants
#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4
#define PKT_INSTANCE_TYPE_REPLICATION 5
#define PKT_INSTANCE_TYPE_RESUBMIT 6
