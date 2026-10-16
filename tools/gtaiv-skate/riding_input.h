// The keyboard feeds the same bounded packet used by the existing Skate Session.
#pragma once
namespace combine_input {
template<class Packet> bool keyboard(Packet& packet,bool permitted,bool push,bool left,bool right) {
    packet={};
    if(!permitted)return false;
    if(push)packet.buttons=0x4000;
    if(left!=right)packet.left[0]=left?-20000:20000;
    return true;
}
}
