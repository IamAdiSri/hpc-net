const bit<16> TYPE_BARC = 0b0010001011110000; // BARC frame 0x22F0
const bit<16> TYPE_UNIC = 0b0010001011110001; // Unicast frame 0x22F1

// BARC constants
const bit<48> BARC_DA = 0x0180C2000000;
const bit<4>  BARC_I  = 0xA;
const bit<4>  BARC_P  = 0xB;

const bit<8> H_ID = 0b10101110; // Host identifier 0xAE
const bit<8> S_ID = 0b11101110; // Spine identifier 0xEE
const bit<8> F_ID = 0b11111110; // Fabric identifier 0xFE
const bit<8> R_ID = 0b10111110; // Rack identifier 0xBE