/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_BARC = 0x22F0;

const bit<8>typeSS=0b11101110; //SS identifier
const bit<8>typeFS=0b11111110; //FS identifier
const bit<8>typeRS=0b10111110; //RS identifier

//sample code for Unicast Flow-Zone Switching, with an intentional bug
//Roger Marks 2023-12-21


/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

header ethernet_t {
    bit<8> addr_header;
    bit<8> pod_id;
    bit<8> rack_id;
    bit<8> server_id;
    bit<8> flow_level_1_id;
    bit<8> flow_level_0_id;
    bit<48> srcAddr;
    bit<16> etherType;
}

header barc_t {
//
}

struct headers {
    ethernet_t   ethernet;
    barc_t       barc;    
}

struct metadata_t {
//
}

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
            TYPE_BARC: parse_barc;
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

    // these are self addresses
    bit<8> switchtype;    //takes value SS, FS, or RS
    bit<8> loc1;          //switch location field 1
    bit<8> loc2;          //switch location field 2
    
    action spine() { //spine switch action
        standard_metadata.egress_spec = (bit<9>)hdr.ethernet.pod_id;
    }

    action fabric(bit<8> podID_switch) { //fabric switch action
        if (hdr.ethernet.pod_id == podID_switch){
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.rack_id;
        }else {
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.flow_level_1_id;
        }
    }

    action rack(bit<8> podID_switch, bit<8> rackID_switch) { //rack switch action
        if (hdr.ethernet.pod_id == podID_switch && hdr.ethernet.rack_id == rackID_switch){
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.server_id;
        }else{
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.flow_level_0_id;
        }
    }
    
    apply {       
 
 		switchtype = typeSS;    //example switch type
		loc1 = 2;               //example switch location
		loc2 = 4;               //example switch location

        if (switchtype == typeSS) {
           spine();            
        }            

        if (switchtype == typeFS) {
           fabric(loc2);            
        }            

        if (switchtype == typeRS) {
           rack(loc1,loc2);            
        }            

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