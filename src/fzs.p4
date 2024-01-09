/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "constants.p4"
#include "headers.p4"

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
            // TYPE_UNIC: parse_unic;  // Unicast headers
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
    bit<9> ingressPort = standard_metadata.ingress_port;

    action barc() { // barc action

        // load switch address
        self.read(self_0, (bit<32>) 0);
        self.read(self_1, (bit<32>) 1);
        self.read(self_2, (bit<32>) 2);

        if (hdr.barc.S == BARC_I) {
            // todo: error check
            if (self_0 == 0b00000000) { // address hasn't been set
                self_0 = R_ID;
                standard_metadata.egress_spec = ingressPort;
            } 
            else { // todo
                hdr.barc.subtype = 0xAA;
                standard_metadata.egress_spec = ingressPort;
            }
        } 
        // else if (hdr.barc.S == BARC_P) {} // todo

        self.write((bit<32>) 0, self_0);
        self.write((bit<32>) 1, self_1);
        self.write((bit<32>) 2, self_2);
    }
    
    apply {
        if (hdr.ethernet.etherType == TYPE_BARC) {
            // process BARC frame
            barc();

        } 
        // else if (hdr.ethernet.etherType == TYPE_UNIC) {
        //     // process Unicast frame

        //     if (hdr.ethernet.f0 == BARC_DA) {
        //         barc();
        //     }
            
        //     switchtype = hdr.barc.switchType;    //example switch type
        //     loc1 = hdr.barc.loc1;                //example switch location
        //     loc2 = hdr.barc.loc2;                //example switch location

        //     if (switchtype == typeSS) {
        //     spine();            
        //     }            

        //     if (switchtype == typeFS) {
        //     fabric(loc1);            
        //     }            

        //     if (switchtype == typeRS) {
        //     rack(loc1,loc2);            
        //     }            
        // }

        return;
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
