from scapy.fields import (BitEnumField, BitField, FieldListField, MACField,
                          XByteField, XShortEnumField)
from scapy.packet import Packet, bind_layers

from lib.constants import *


class CEther(Packet):
    """
    Custom ethernet headers
    """

    name = "CustomEthPacket"
    fields_desc = [
        MACField("dst", None),
        MACField("src", None),
        XShortEnumField("type", TYPE_UNIC, {TYPE_BARC: "BARC", TYPE_UNIC: "UNIC"}),
    ]


class BARC(Packet):
    """
    BARC headers
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
    ]


class UNIC(Packet):
    """
    Unicast headers

    TODO
    """

    name = "UNICPacket"
    fields_desc = [
        XByteField("subtype", 0x00),
        BitField("h", 0b0, 1),
        BitField("version", 0b000, 3),
        BitEnumField("S", BARC_I, 4, {BARC_I: "I", BARC_P: "P"}),
        FieldListField("BI", [], XByteField("", 0x00), count_from=lambda pkt: 6),
        BitField("BA", 0x000000000000, 48),
        BitField("Info", 0x000000000000, 48),
    ]


bind_layers(CEther, BARC, type=TYPE_BARC)
bind_layers(CEther, UNIC, type=TYPE_UNIC)


def deparser(pkt):
    """
    Takes an arbitrary pkt and deparses 
    it to fit the CEther frame.
    """
    raw = bytes(pkt)
    return CEther(raw)
