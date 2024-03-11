/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


/* -*- P4_16 -*- */

control SFZSEgress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    // switch address placeholders
    // bit<8> self_0;        // switch type
    // bit<8> self_1;        // switch location field 1
    // bit<8> self_2;        // switch location field 2

    apply { 
        // if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_CLONE || standard_metadata.egress_spec == CTRL_PORT) {
        //     if (hdr.ethernet.dstAddr == NCB_DA && hdr.ethernet.etherType == TYPE_CORE) {
        //         // load switch address
        //         self.read(self_0, (bit<32>) 0);
        //         self.read(self_1, (bit<32>) 1);
        //         self.read(self_2, (bit<32>) 2);
                
        //         if (self_0 == RCK_ID) {
        //             hdr.proto.core.inport = hdr.ethernet.srcAddr.f3;
        //         }
        //         else if (self_0 == FAB_ID) {
        //             hdr.proto.core.inport = hdr.ethernet.srcAddr.f2;
        //         }
        //         else if (self_0 == SPN_ID) {
        //             hdr.proto.core.inport = hdr.ethernet.srcAddr.f1;
        //         }
        //         else {
        //             log_msg("ERROR: Unknown CoRe switch ID; packet dropped.");
        //             standard_metadata.egress_spec = DROP_PORT;
        //         }
        //     }
        // }
     }
}