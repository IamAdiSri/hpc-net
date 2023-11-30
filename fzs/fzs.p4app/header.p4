#ifndef __HEADER_P4__
#define __HEADER_P4__ 1

struct omniran_metadata_t {
    bit<8> id_1;
    bit<8> id_2;
}

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


struct metadata {
    @name("omniran_metadata")
    omniran_metadata_t   omniran_metadata;
}

struct headers {
    @name("ethernet")
    ethernet_t ethernet;
}

#endif // __HEADER_P4__
