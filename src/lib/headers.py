# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from lib.constants import *
from scapy.fields import (BitEnumField, BitField, FieldListField, MACField,
                          StrField, XByteField, XShortEnumField)
from scapy.packet import Packet, bind_layers


class CEther(Packet):
    """
    Custom ethernet header
    """

    name = "CustomEthPacket"
    fields_desc = [
        MACField("dst", None),
        MACField("src", None),
        XShortEnumField("type", None, {TYPE_BARC: "BARC", TYPE_CORE: "CORE"}),
    ]


class BARC(Packet):
    """
    BARC header
    """

    name = "BARCPacket"
    fields_desc = [
        XByteField("subtype", 0x00),
        BitField("h", 0b0, 1),
        BitField("version", 0b000, 3),
        BitEnumField("S", BARC_I, 4, {BARC_I: "I", BARC_P: "P"}),
        FieldListField("BI", [], XByteField("", 0x00), count_from=lambda pkt: 6),
        BitField("BA", 0x000000000000, 48),
        BitField("Info", 0x000000000000, 48),
        # TODO: FCS Field
    ]


class CORE(Packet):
    """
    CoRe header
    """

    name = "COREPacket"
    fields_desc = [
        BitField("subtype", CORE_S, 16),
        FieldListField("CA", [], XByteField("", 0x00), count_from=lambda pkt: 6),
        # TODO: FCS field
        # Exception while parsing: PacketTooShort
        BitField("swaddr", 0x000000, 24),
        BitField("inport", 0x00, 8),
    ]


bind_layers(CEther, BARC, type=TYPE_BARC)
bind_layers(CEther, CORE, type=TYPE_CORE)


def deparser(pkt):
    """
    Takes an arbitrary packet and deparses
    it to fit the CEther frame.
    """

    return CEther(bytes(pkt))
