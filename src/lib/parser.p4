/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


/* -*- P4_16 -*- */

parser SFZSParser(packet_in packet, out headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_BARC: parse_barc;  // BARC headers
            TYPE_CORE: parse_core;  // CORE headers
            default: accept;
        }
    }

    state parse_barc {
        packet.extract(hdr.proto.barc);
        transition accept;
    }

    
    state parse_core {
        packet.extract(hdr.proto.core);
        transition accept;
    }
}