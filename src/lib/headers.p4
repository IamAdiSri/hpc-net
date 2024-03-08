/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */


/* -*- P4_16 -*- */

// 48-bit flow-zone address
struct addr_t {
    bit<8> f0;
    bit<8> f1;
    bit<8> f2;
    bit<8> f3;
    bit<8> f4;
    bit<8> f5;
}

// ethernet header
header ethernet_t {
    addr_t  dstAddr;
    addr_t  srcAddr;
    bit<16> etherType;
}

// barc header
header barc_t{
    bit<8>  subtype;
    bit<1>  h;
    bit<3>  version;
    bit<4>  S;
    addr_t  BI;
    bit<48> BA;
    bit<48> Info;
    // TODO: FCS field
}

// core header
header core_t{
    bit<16> subtype;
    addr_t  CA;
    // TODO: FCS field
    bit<24> swaddr;
    bit<8> inport;
}

// combined special headers
header_union proto_t {
    barc_t barc;
    core_t core;
}

// complete packet header
struct headers {
    ethernet_t ethernet;
    proto_t proto;
}

// metadata
struct metadata_t {
}