/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


/* -*- P4_16 -*- */

control SFZSIngress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    
    // switch address placeholders
    bit<8> self_0;        // switch type
    bit<8> self_1;        // switch location field 1
    bit<8> self_2;        // switch location field 2

    // record the ingress port
    bit<8> ingressPort = standard_metadata.ingress_port[7:0];

    // calculate direction of ingress port
    // ingressPort <  TREE_K/2 is low
    // ingressPort >= TREE_K/2 is high
    bool ingressDir = ingressPort < TREE_K/2;

    // egress port
    bit<8> egressPort;

    action drop() {
        // sets egress port to DROP_PORT unless specified 
        // otherwise with the --drop-port flag
        
        // same as the following:
        // standard_metadata.egress_spec = DROP_PORT;


        mark_to_drop(standard_metadata);
    }

    action barc_i_rs() {
        
        // calculate egress port
        egressPort = ingressPort + TREE_K/2;

        // modify frame
        hdr.proto.barc.S = BARC_P;
        hdr.proto.barc.BI.f0 = FAB_ID;
        hdr.proto.barc.BI.f1 = 0;
        hdr.proto.barc.BI.f2 = ingressPort;
        hdr.proto.barc.BI.f3 = 0;
        hdr.proto.barc.BI.f4 = 0;
        hdr.proto.barc.BI.f5 = 0xFF;

        // set egress port
        standard_metadata.egress_spec = (bit <9>) egressPort;
    }

    action barc_p_rs() {

        if (self_0 == 0x00 || 
            (self_0 == hdr.proto.barc.BI.f0 &&
             self_1 == hdr.proto.barc.BI.f1 &&
             self_2 == hdr.proto.barc.BI.f2)) { // address hasn't been set or 
                                          // has been set correctly
            
            // calculate egress port
            egressPort = ingressPort - TREE_K/2;
            
            // set address
            self_0 = hdr.proto.barc.BI.f0;
            self_1 = hdr.proto.barc.BI.f1;
            self_2 = hdr.proto.barc.BI.f2;

            // modify frame
            hdr.proto.barc.S = BARC_P;
            hdr.proto.barc.BI.f0 = HST_ID;
            hdr.proto.barc.BI.f1 = self_1;
            hdr.proto.barc.BI.f2 = self_2;
            hdr.proto.barc.BI.f3 = egressPort;
            hdr.proto.barc.BI.f4 = 0;
            hdr.proto.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = (bit <9>) egressPort;
        }
        else { // address has been set incorrectly
            
            // mark to drop
            standard_metadata.egress_spec = DROP_PORT;

        }
    }

    action barc_p_fs_low() {

        // calculate egress port
        egressPort = ingressPort + TREE_K/2;

        // modify frame
        hdr.proto.barc.S = BARC_P;
        hdr.proto.barc.BI.f0 = SPN_ID;
        hdr.proto.barc.BI.f1 = ingressPort;
        hdr.proto.barc.BI.f2 = self_2;
        hdr.proto.barc.BI.f3 = 0;
        hdr.proto.barc.BI.f4 = 0;
        hdr.proto.barc.BI.f5 = 0;

        // set egress port
        standard_metadata.egress_spec = (bit <9>) egressPort;
    }

    action barc_p_fs_high() {

        if (self_0 == 0x00 || 
           (self_0 == hdr.proto.barc.BI.f0 &&
            self_1 == hdr.proto.barc.BI.f1 &&
            self_2 == hdr.proto.barc.BI.f2)) {
                        // address hasn't been set or 
                        // has been set correctly
            
            // calculate egress port
            egressPort = ingressPort - TREE_K/2;

            // set address
            self_0 = hdr.proto.barc.BI.f0;
            self_1 = hdr.proto.barc.BI.f1;
            self_2 = hdr.proto.barc.BI.f2;

            // modify frame
            hdr.proto.barc.S = BARC_P;
            hdr.proto.barc.BI.f0 = RCK_ID;
            hdr.proto.barc.BI.f1 = self_1;
            hdr.proto.barc.BI.f2 = egressPort;
            hdr.proto.barc.BI.f3 = 0;
            hdr.proto.barc.BI.f4 = 0;
            hdr.proto.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = (bit <9>) egressPort;
        } 
        else { // address has been set incorrectly

            // mark to drop
            standard_metadata.egress_spec = DROP_PORT;
        }
        
    }

    action barc_p_ss() {
        
        if (self_0 == 0x00 || 
           (self_0 == hdr.proto.barc.BI.f0 &&
            self_1 == hdr.proto.barc.BI.f1 &&
            self_2 == hdr.proto.barc.BI.f2)) {
                            // address hasn't been set or 
                            // has been set correctly
            
            // calculate egress port
            // egressPort = (ingressPort + TREE_K/2) % TREE_K;

            // can't use modulo here as it is
            // only supported at compile time
            egressPort = ingressPort + TREE_K/2;
            if (egressPort >= TREE_K){
                egressPort = egressPort - TREE_K;
            }

            // set address
            self_0 = hdr.proto.barc.BI.f0;
            self_1 = hdr.proto.barc.BI.f1;
            self_2 = hdr.proto.barc.BI.f2;

            // modify frame
            hdr.proto.barc.S = BARC_P;
            hdr.proto.barc.BI.f0 = FAB_ID;
            hdr.proto.barc.BI.f1 = egressPort;
            hdr.proto.barc.BI.f2 = self_2;
            hdr.proto.barc.BI.f3 = 0;
            hdr.proto.barc.BI.f4 = 0;
            hdr.proto.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = (bit <9>) egressPort;
        }
        else { // address has been set incorrectly
            
            // mark to drop
            standard_metadata.egress_spec = DROP_PORT;
        }
    }

    action multicast_to_group(bit<16> mc_group) {
        standard_metadata.mcast_grp = mc_group;
    }

    action multicast_registration(bit<8> switchPort) {
        // send packet to switch
        standard_metadata.egress_spec = (bit<9>) switchPort;

        // send clone to controller
        clone(CloneType.I2E, CTRL_SESSION);
    }

    action placeholder_action() {}

    table mc_table {
        key = {
            hdr.ethernet.dstAddr.f0 : exact;
            hdr.ethernet.dstAddr.f1 : exact;
            hdr.ethernet.dstAddr.f2 : exact;
            hdr.ethernet.dstAddr.f3 : exact;
            hdr.ethernet.dstAddr.f4 : exact;
            hdr.ethernet.dstAddr.f5 : exact;
            ingressPort: exact;
        }
        actions = {
            multicast_to_group;
        }
        // size = 1024;
    }

    table placeholder_table {
        key = {
            hdr.proto.core.CA.f0 : exact;
            hdr.proto.core.CA.f1 : exact;
            hdr.proto.core.CA.f2 : exact;
            hdr.proto.core.CA.f3 : exact;
            hdr.proto.core.CA.f4 : exact;
            hdr.proto.core.CA.f5 : exact;
            ingressPort: exact;
        }
        actions = {
            placeholder_action;
        }
    }
    
    apply {
        
        log_msg("Source Address: {}:{}:{}:{}:{}:{}", hdr.ethernet.srcAddr);

        if (hdr.ethernet.dstAddr.f0 == HST_ID) { // unicast

            log_msg("Unicast DA: {}:{}:{}:{}:{}:{}", hdr.ethernet.dstAddr);

            // load switch address
            self.read(self_0, (bit<32>) 0);
            self.read(self_1, (bit<32>) 1);
            self.read(self_2, (bit<32>) 2);

            if (self_0 == RCK_ID) { // rack switch

                if (hdr.ethernet.dstAddr.f1 == self_1 &&
                    hdr.ethernet.dstAddr.f2 == self_2) {
                    
                    standard_metadata.egress_spec = (bit<9>) hdr.ethernet.dstAddr.f3;
                }
                else {

                    standard_metadata.egress_spec = (bit<9>) hdr.ethernet.dstAddr.f5 + TREE_K/2;
                }
            }
            else if (self_0 == FAB_ID) { // fabric switch

                if (hdr.ethernet.dstAddr.f1 == self_1) {
                    
                    standard_metadata.egress_spec = (bit<9>) hdr.ethernet.dstAddr.f2;
                }
                else {
                    
                    standard_metadata.egress_spec = (bit<9>) hdr.ethernet.dstAddr.f4 + TREE_K/2;
                }
            }
            else if (self_0 == SPN_ID) { // spine switch

                standard_metadata.egress_spec = (bit<9>) hdr.ethernet.dstAddr.f1;
            }
            else { // unknown switch

                log_msg("ERROR: Unknown unicast switch ID; packet dropped.");
                standard_metadata.egress_spec = DROP_PORT;
            }
        }
        else if (hdr.ethernet.dstAddr.f0 == (SPN_ID | 1)) { // multicast forwarding

            log_msg("Multicast DA: {}:{}:{}:{}:{}:{}", hdr.ethernet.dstAddr);

            if (!mc_table.apply().hit) { // no match found
                log_msg("WARNING: Did not find a match for the multicast address; packet dropped.");
                standard_metadata.egress_spec = DROP_PORT;
            }
        }
        else if (hdr.ethernet.dstAddr == NCB_DA) { // special multicast

            if (hdr.ethernet.etherType == TYPE_BARC) { // BARC

                log_msg("BARC DA: {}:{}:{}:{}:{}:{}", hdr.ethernet.dstAddr);

                if (hdr.proto.barc.S == BARC_I) { // BARC Inquiry
                    barc_i_rs();
                }
                else if (hdr.proto.barc.S == BARC_P) { // BARC Proposal

                    // load switch address
                    self.read(self_0, (bit<32>) 0);
                    self.read(self_1, (bit<32>) 1);
                    self.read(self_2, (bit<32>) 2);

                    if (hdr.proto.barc.BI.f0 == FAB_ID) { // to fabric switch
                        if (ingressDir) {
                            // low port of ingress
                            barc_p_fs_low();
                        }
                        else {
                            // high port of ingress
                            barc_p_fs_high();
                        }
                    }
                    else if (hdr.proto.barc.BI.f0 == RCK_ID) { // to rack switch
                        barc_p_rs();
                    }
                    else if (hdr.proto.barc.BI.f0 == SPN_ID) { //  to spine switch
                        barc_p_ss();
                    }
                    else { // unknown switch type
                    
                        log_msg("ERROR: Unknown BARC switch ID; packet dropped.");
                        standard_metadata.egress_spec = DROP_PORT;
                    }

                    // update switch address 
                    self.write((bit<32>) 0, self_0);
                    self.write((bit<32>) 1, self_1);
                    self.write((bit<32>) 2, self_2);
                }
                else { // unknown BARC subtype

                    log_msg("ERROR: Unknown BARC subtype; packet dropped.");
                    standard_metadata.egress_spec = DROP_PORT;
                }
            }
            else if (hdr.ethernet.etherType == TYPE_CORE) { // Collective Registration (CoRe)

                if (hdr.proto.core.subtype == CORE_S) { // collective registration

                    log_msg("CoRe CA: {}:{}:{}:{}:{}:{}", hdr.proto.core.CA);

                    if (!placeholder_table.apply().hit) { // match not found
                                                          // add (ca, ingress port)
                        
                        // load switch address
                        self.read(self_0, (bit<32>) 0);
                        self.read(self_1, (bit<32>) 1);
                        self.read(self_2, (bit<32>) 2);

                        if (self_0 == RCK_ID) { // rack switch
                            multicast_registration(hdr.proto.core.CA.f2 + TREE_K/2);
                        }
                        else if (self_0 == FAB_ID) { // fabric switch
                            multicast_registration(hdr.proto.core.CA.f1 + TREE_K/2);
                        }
                        else if (self_0 == SPN_ID) { // spine switch
                            // this doesn't work for some reason on spine switches
                            // multicast_registration(DROP_PORT);

                            // send packet to switch
                            standard_metadata.egress_spec = (bit<9>) CTRL_PORT;
                        }
                        else { // unknown switch
                            
                            log_msg("ERROR: Unknown CoRe switch ID; packet dropped.");
                            standard_metadata.egress_spec = DROP_PORT;
                        }
                    }
                    else { // match found
                        log_msg("WARNING: Host is already a member of the collective; packet dropped.");
                        standard_metadata.egress_spec = DROP_PORT;
                    }
                }
                else {
                    // TODO: For future use
                }
            }
            else { // unknown etherType
                log_msg("ERROR: Unknown multicast ethertype; packet dropped.");
                standard_metadata.egress_spec = DROP_PORT;
            }
        }
        else { // unknown protocol
            log_msg("ERROR: Unknown address; packet dropped");
            standard_metadata.egress_spec = DROP_PORT;
        }
    }
}
