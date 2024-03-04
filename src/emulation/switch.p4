/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


/* -*- P4_16 -*- */

#include <core.p4>
#include <v1model.p4>

#include "../lib/headers.p4"
#include "../lib/constants.p4"
#include "../lib/registers.p4"
#include "runtime.p4"

#include "../lib/parser.p4"
#include "../lib/ingress.p4"
#include "../lib/deparser.p4"

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata_t meta) {   
    apply {  }
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
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
    SFZSParser(),
    MyVerifyChecksum(),
    SFZSIngress(),
    MyEgress(),
    MyComputeChecksum(),
    SFZSDeparser()
) main;
