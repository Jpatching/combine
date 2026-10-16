// Opt-in evaluation input at the GTA -> worker packet boundary.
// The plugin holds its ownership lock around these calls. No IO or simulation.
#pragma once
#include <cstdint>

class EvaluationInput {
    int profile_=0;
    uint32_t started_=0,duration_=0;
public:
    void clear() {duration_=0;}
    bool arm(int profile,int duration,uint32_t now) {
        clear();
        if(profile<0 || profile>3 || duration<50 || duration>1000)return false;
        profile_=profile;started_=now;duration_=static_cast<uint32_t>(duration);
        return true;
    }
    template<class Packet> bool apply(Packet& packet,bool allowed,uint32_t now) {
        if(!allowed || !duration_ || now-started_>=duration_) {clear();return false;}
        packet={};
        if(profile_>0)packet.buttons=0x4000; // XInput X, unchanged Skate input.
        if(profile_==2)packet.left[0]=-20000;
        if(profile_==3)packet.left[0]=20000;
        return true;
    }
};
