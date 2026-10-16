#include "../evaluation_input.h"
#include <cassert>
#include <cstdint>
#include <iostream>

struct Packet {
    uint16_t buttons; int16_t left[2],right[2]; uint8_t triggers[2];
};

int main() {
    EvaluationInput playback;
    Packet packet{};
    assert(playback.arm(1,100,1000));
    assert(playback.apply(packet,true,1000));
    assert(packet.buttons==0x4000); // XInput X: actual Skate push input.
    packet={};
    assert(!playback.apply(packet,true,1100));
    assert(packet.buttons==0);
    std::cout<<"PASS: evaluation push expires at its deadline\n";

    assert(playback.arm(2,100,2000));
    assert(playback.apply(packet,true,2000));
    assert(packet.buttons==0x4000 && packet.left[0]==-20000);
    packet={};
    assert(!playback.apply(packet,false,2050));
    assert(!playback.apply(packet,true,2051));
    assert(packet.buttons==0 && packet.left[0]==0);
    std::cout<<"PASS: loss of permission cancels playback until explicitly rearmed\n";

    assert(playback.arm(3,100,0xfffffff0u));
    assert(playback.apply(packet,true,0x20u));
    assert(packet.left[0]==20000);
    assert(!playback.apply(packet,true,0x54u));
    assert(playback.arm(1,100,3000));
    assert(!playback.arm(4,100,3000));
    assert(!playback.apply(packet,true,3001));
    assert(!playback.arm(1,1001,3000));
    assert(!playback.arm(1,49,3000));
    assert(playback.arm(0,100,3000));
    assert(playback.apply(packet,true,3001));
    assert(packet.buttons==0 && packet.left[0]==0);
    playback.clear();
    assert(!playback.apply(packet,true,3002));
    std::cout<<"PASS: clock wrap, bounded profiles, neutral and explicit cancellation\n";
}
