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
    bit<9> ingressPort = standard_metadata.ingress_port;

    // calculate direction of ingress port
    // msb = 0 is low and msb = 1 is high
    // therefore, low ports start from 0 and
    // high ports start from 256
    bit<1> ingressDir = (ingressPort >> 8)[0:0];

    // calculate egress port
    bit<9> egressPort = ingressPort ^ (1<<8);

    action barc_i_rs() {

        // modify frame
        hdr.barc.S = BARC_P;
        hdr.barc.BI.f0 = FAB_ID;
        hdr.barc.BI.f1 = egressPort[7:0];
        hdr.barc.BI.f2 = 0;
        hdr.barc.BI.f3 = 0;
        hdr.barc.BI.f4 = 0;
        hdr.barc.BI.f5 = 0xFF;

        // set egress port
        standard_metadata.egress_spec = egressPort;
    }

    action barc_p_rs() {

        if (self_0 == 0x00 || 
            (self_0 == hdr.barc.BI.f0 &&
             self_1 == hdr.barc.BI.f1 &&
             self_2 == hdr.barc.BI.f2)) { // address hasn't been set or 
                                          // has been set correctly
            
            // set address
            self_0 = hdr.barc.BI.f0;
            self_1 = hdr.barc.BI.f1;
            self_2 = hdr.barc.BI.f2;

            // modify frame
            hdr.barc.S = BARC_P;
            hdr.barc.BI.f0 = HST_ID;
            hdr.barc.BI.f1 = hdr.barc.BI.f1;
            hdr.barc.BI.f2 = hdr.barc.BI.f2;
            hdr.barc.BI.f3 = egressPort[7:0];
            hdr.barc.BI.f4 = 0;
            hdr.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = egressPort;
        }
        else { // address has been set incorrectly
            
            // TODO: raise error
            // mark to drop?
            standard_metadata.egress_spec = 72;

        }
    }

    action barc_p_fs_low() {

        if (self_0 == 0x00 || 
            (self_0 == hdr.barc.BI.f0 && 
             self_1 == hdr.barc.BI.f1)) {
                    // address hasn't been set or 
                    // has been set correctly

            // set address
            self_0 = hdr.barc.BI.f0;
            self_1 = hdr.barc.BI.f1;

            // modify frame
            hdr.barc.S = BARC_P;
            hdr.barc.BI.f0 = SPN_ID;
            hdr.barc.BI.f1 = hdr.barc.BI.f1;
            hdr.barc.BI.f2 = egressPort[7:0];
            hdr.barc.BI.f3 = 0;
            hdr.barc.BI.f4 = 0;
            hdr.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = egressPort;
        } 
        else { // address has been set incorrectly

            // TODO: raise error
            // mark to drop?
            standard_metadata.egress_spec = 69;
        }
    }

    action barc_p_fs_high() {

        if (self_2 == 0x00 || self_2 == hdr.barc.BI.f2) {
                        // address hasn't been set or 
                        // has been set correctly

            // set address
            self_2 = hdr.barc.BI.f2;

            // modify frame
            hdr.barc.S = BARC_P;
            hdr.barc.BI.f0 = RCK_ID;
            hdr.barc.BI.f1 = hdr.barc.BI.f2;
            hdr.barc.BI.f2 = egressPort[7:0];
            hdr.barc.BI.f3 = 0;
            hdr.barc.BI.f4 = 0;
            hdr.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = egressPort;
        } 
        else { // address has been set incorrectly

            // TODO: raise error
            // mark to drop?
            standard_metadata.egress_spec = 70;
        }
        
    }

    action barc_p_ss() {
        
        if (self_0 == 0x00 || 
            (self_0 == hdr.barc.BI.f0 &&
                self_1 == hdr.barc.BI.f1 &&
                self_2 == hdr.barc.BI.f2)) {
                            // address hasn't been set or 
                            // has been set correctly
            
            // set address
            self_0 = hdr.barc.BI.f0;
            self_1 = hdr.barc.BI.f1;
            self_2 = hdr.barc.BI.f2;

            // modify frame
            hdr.barc.S = BARC_P;
            hdr.barc.BI.f0 = FAB_ID;
            hdr.barc.BI.f1 = hdr.barc.BI.f1;
            hdr.barc.BI.f2 = egressPort[7:0];
            hdr.barc.BI.f3 = 0;
            hdr.barc.BI.f4 = 0;
            hdr.barc.BI.f5 = 0;

            // set egress port
            standard_metadata.egress_spec = egressPort;
        }
        else { // address has been set incorrectly
            
            // TODO: raise error
            // mark to drop?
            standard_metadata.egress_spec = 71;
        }
    }
    
    apply {
        if (hdr.ethernet.etherType == TYPE_BARC || 
            hdr.ethernet.dstAddr == BARC_DA) { // process BARC frame

            if (hdr.barc.S == BARC_I) { // BARC Inquiry
                barc_i_rs();
            }
            else if (hdr.barc.S == BARC_P) { // BARC Proposal

                // load switch address
                self.read(self_0, (bit<32>) 0);
                self.read(self_1, (bit<32>) 1);
                self.read(self_2, (bit<32>) 2);

                if (hdr.barc.BI.f0 == FAB_ID) { // to fabric switch
                    if (ingressDir == 0) {
                        // low port of ingress
                        barc_p_fs_low();
                    }
                    else {
                        // high port of ingress
                        barc_p_fs_high();
                    }
                }
                else if (hdr.barc.BI.f0 == RCK_ID) { // to rack switch
                    barc_p_rs();
                }
                else if (hdr.barc.BI.f0 == SPN_ID) { //  to spine switch
                    barc_p_ss();
                }
                else { // unknown switch type
                    // TODO: raise error
                    // mark to drop?
                    standard_metadata.egress_spec = 73;
                }

                // update switch address 
                self.write((bit<32>) 0, self_0);
                self.write((bit<32>) 1, self_1);
                self.write((bit<32>) 2, self_2);
            }
            else { // unknown BARC type

                // TODO: raise error
                // mark to drop?
                standard_metadata.egress_spec = 74;
            }
        }
    }
}