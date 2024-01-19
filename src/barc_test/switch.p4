/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "../lib/headers.p4"
#include "../lib/constants.p4"
#include "runtime.p4" // generated at runtime

// Three 8-bit registers for global addressing
register<bit<8>>(3) self;

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet, out headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_BARC: parse_barc;  // BARC headers
            default: accept;
        }
    }

    state parse_barc {
        packet.extract(hdr.barc);
        transition accept;
    }
}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata_t meta) {   
    apply {  }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

    // switch address placeholders
    bit<8> self_0;        // switch type
    bit<8> self_1;        // switch location field 1
    bit<8> self_2;        // switch location field 2

    // record the ingress port
    // bit<8> ingressPort = standard_metadata.ingress_port[7:0];
    bit<9> ingressPort = standard_metadata.ingress_port;

    // calculate egress port
    // bit<8> egressPort = ingressPort ^ 0b100000000;
    // bit<8> egressPort = ingressPort ^ (1<<7);
    bit<9> egressPort = ingressPort ^ (1<<8);

    action barc() {
        // load switch address
        self.read(self_0, (bit<32>) 0);
        self.read(self_1, (bit<32>) 1);
        self.read(self_2, (bit<32>) 2);

        if (hdr.barc.S == BARC_I) { // BARC Inquiry

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
        else if (hdr.barc.S == BARC_P) { // BARC Proposal

            if (hdr.barc.BI.f0 == FAB_ID) { // to fabric switch

                // calculate direction of ingress port
                // msb = 0 is low and msb = 1 is high
                // therefore, low ports start from 0 and
                // high ports start from 256
                bit<1> ingressDir = ((ingressPort >> 7) & 0b1)[0:0];

                if (ingressDir == 0) { // low port of ingress

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
                    }

                }
                else { // high port of ingress

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
                    }

                }

            }
            else if (hdr.barc.BI.f0 == SPN_ID) { // to spine switch

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

                }

            }
            else if (hdr.barc.BI.f0 == RCK_ID) { // to rack switch

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

                }
            }
            else { // unknown switch type

                // TODO: raise error
                // mark to drop?

            }
        }
        else { // unknown BARC type

            // TODO: raise error
            // mark to drop?
        }

        // update switch address (needs to be uncommented in non-test version)
        // self.write((bit<32>) 0, self_0);
        // self.write((bit<32>) 1, self_1);
        // self.write((bit<32>) 2, self_2);        

        return;
    }
    
    apply {
        if (hdr.ethernet.etherType == TYPE_BARC || 
            hdr.ethernet.dstAddr == BARC_DA) {
            // process BARC frame
            barc();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata_t meta) {
     apply {  }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.barc);        
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
