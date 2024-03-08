control SFZSEgress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

    apply {
        log_msg("Received at egress, instance_type = {}!", {standard_metadata.instance_type});
        if (standard_metadata.instance_type == 1) {
            log_msg("Received at egress!");
            standard_metadata.egress_spec = CTRL_PORT;
        }
    }
}