// frame types
const bit<16> TYPE_BARC = 0x22F0; // BARC frame 0b0010001011110000
const bit<16> TYPE_UNIC = 0x22F1; // Unicast frame 0b0010001011110001

// BARC constants
const bit<48> BARC_DA = 0x0180C2000000;
const bit<4>  BARC_I  = 0xA;
const bit<4>  BARC_P  = 0xB;

// node identifiers
const bit<8> HST_ID = 0xAE; // Host identifier 0b10101110
const bit<8> SPN_ID = 0xEE; // Spine identifier 0b11101110
const bit<8> FAB_ID = 0xFE; // Fabric identifier 0b11111110
const bit<8> RCK_ID = 0xBE; // Rack identifier 0b10111110