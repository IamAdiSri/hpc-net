#include <core.p4>
#include <v1model.p4>

#include "header.p4"
#include "parser.p4"

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply { }
}
control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    action _drop() {
        mark_to_drop();
    }
    action spine() {
        standard_metadata.egress_spec = (bit<9>)hdr.ethernet.pod_id;
    }
    action fabric(bit<8> id_1) {
        if (hdr.ethernet.pod_id == id_1){
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.rack_id;
        }else {
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.flow_level_0_id;
        }
    }
    action rack(bit<8> id_1, bit<8> id_2) {
        if (hdr.ethernet.pod_id == id_2 && hdr.ethernet.rack_id == id_1){
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.server_id;
        }else{
            standard_metadata.egress_spec = (bit<9>)hdr.ethernet.flow_level_1_id;
        }
    }
    table identification {
        actions = {
            spine;
            fabric;
            rack;
            _drop;
        }
        key = {
            // hdr.ethernet.addr_header: exact;
        }
        size = 2;
    }
    apply {
        identification.apply();
    }
}
V1Switch(ParserImpl(), verifyChecksum(), ingress(), egress(), computeChecksum(), DeparserImpl()) main;
