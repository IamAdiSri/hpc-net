control SFZSEgress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    apply { 
        // log_msg("EGRESS RECEIVED: {}", {standard_metadata.instance_type});
        // if (standard_metadata.instance_type == 1) {
        //     if (hdr.ethernet.dstAddr == NCB_DA) {
        //         hdr.proto.core.inport = standard_metadata.ingress_port[7:0];
        //     }
        //     // log_msg("EGRESS SPEC = {}", {standard_metadata.egress_spec});
        // }
     }
}