// simple.p4
// This program defines a simple L2 switch that forwards packets based on the destination MAC address.
// simple_switch.p4
// simple_switch.p4
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

parser MyParser(packet_in packet,
                out ethernet_t hdr) {
    state start {
        packet.extract(hdr);
        transition accept;
    }
}

control MyIngress(inout ethernet_t hdr,
                  inout metadata_t meta) {
    apply {
        if (hdr.dstAddr == 48'h123456789abc) {
            meta.outputPort = 1;
        } else {
            meta.outputPort = 2;
        }
    }
}

V1Switch(MyParser(), MyIngress())

// compile with: p4c-bm2-ss simple.p4 -o simple.json --p4runtime-files simple.p4info
// run with: simple_switch -i 0@eth1 -i 1@eth2 simple.json
