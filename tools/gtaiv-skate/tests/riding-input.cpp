#include "../riding_input.h"
#include <cassert>
#include <cstdint>
#include <iostream>

struct Packet {uint16_t buttons; int16_t left[2],right[2]; uint8_t triggers[2];};
int main() {
    Packet packet{};
    assert(combine_input::keyboard(packet,true,true,true,false));
    assert(packet.buttons==0x4000 && packet.left[0]==-20000);
    assert(packet.right[0]==0 && packet.triggers[0]==0);
    assert(combine_input::keyboard(packet,true,false,false,true));
    assert(packet.buttons==0 && packet.left[0]==20000);
    assert(combine_input::keyboard(packet,true,true,true,true));
    assert(packet.buttons==0x4000 && packet.left[0]==0);
    assert(!combine_input::keyboard(packet,false,true,true,false));
    assert(packet.buttons==0 && packet.left[0]==0);
    std::cout<<"PASS: W push, A/D steering, opposing keys neutral and focus-loss clearing\n";
}
