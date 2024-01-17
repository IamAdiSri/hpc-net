/*
**  DO NOT MAKE CHANGES TO THIS FILE
**  
**  This file is dynamically overwritten at runtime by
**  network.py and changes to this file do not persist 
**  across runs.
*/ 

// K for K-ary tree
const int TREE_K = 4;

// encode the direction of the ports
// by setting the i-th bit to 1 or 0 
// depending on whether the i-th port
// is high or low respectively 
// (generally half and half split).
// const bit<TREE_K> PORT_DIR = 0b0011;
const bit<4> PORT_DIR = 0b0011;
