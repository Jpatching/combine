// Standalone authored-surface Session proof for explicitly selected native backend.
// Never attaches to or controls GTA; literal test geometry is not qualification.
#include <windows.h>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdint>
#include <cstring>
extern "C" {
struct Packet {uint16_t buttons;int16_t left[2],right[2];uint8_t triggers[2];};
int combine_config(const wchar_t*,uint32_t);void combine_stop();int combine_vertex(float,float,float);
int combine_mount(float,float,float,float,float);int combine_poll();int combine_tick(uint32_t,float,const Packet*);float combine_value(int);
int combine_surface_begin(uint32_t,uint32_t);int combine_surface_vertex(float,float,float);
int combine_mount_surface(float,float,float,float,float,uint32_t,uint32_t);
int combine_tick_surface(uint32_t,float,float,float,uint32_t,uint32_t,const Packet*);
}
using Time=std::chrono::steady_clock;
static double maximum=0;
static bool workerBackend=false;
static const char* phase="initialization";
static unsigned ticks=0;
static DWORD previousTick=0;
static double maximumTick=0;
static DWORD maximumGap=0;
static void configure() {
    wchar_t exe[32768];const auto length=GetModuleFileNameW(nullptr,exe,32768);
    if(!length || !combine_config(exe,length))throw "configuration refused";
}
template<class F> int bounded(F action) {const auto start=Time::now();const int result=action();const double ms=std::chrono::duration<double,std::milli>(Time::now()-start).count();if(ms>maximum)maximum=ms;if(workerBackend && ms>50)throw "blocking worker parent call";return result;}
// Literal authored triangles, not game geometry. The independent observation
// formula below describes the known plane at the last displayed query position.
static constexpr uint32_t surfaceLayer=7;
static float authored_ground(float x,float y) {return 10.f+0.05f*(x-100.f)+0.1f*(y-200.f);}
static void surface_upload(uint32_t triangles=2) {
    if(!combine_surface_begin(surfaceLayer,triangles))throw "surface upload begin refused";
    const float vertices[][3]={{68,168,5.2f},{132,168,8.4f},{132,232,14.8f},
                              {68,168,5.2f},{132,232,14.8f},{68,232,11.6f}};
    for(uint32_t pair=0;pair<triangles/2;pair++)
        for(const auto& v:vertices)if(!combine_surface_vertex(v[0],v[1],v[2]))throw "surface triangle vertex refused";
}
static void surface_mount() {
    previousTick=0;
    combine_stop();Sleep(100);configure();
    surface_upload();
    const int prepared=bounded([]{return combine_mount_surface(100,200,10,0,1,surfaceLayer,1);});
    if(prepared!=(workerBackend?2:1))throw "selected backend preparation contract mismatch";
    const auto start=Time::now();int state=prepared;
    while(state==2 && Time::now()-start<std::chrono::seconds(60)) {state=bounded([]{return combine_poll();});Sleep(5);}
    if(state!=1)throw "surface preparation unavailable";
}
static void surface_tick(const Packet& packet) {
    ++ticks;
    const float x=combine_value(0),y=combine_value(1);
    if(!std::isfinite(x)||!std::isfinite(y))throw "surface query pose unavailable";
    const DWORD now=GetTickCount();
    if(previousTick && now-previousTick>maximumGap)maximumGap=now-previousTick;
    previousTick=now;
    const auto tickStart=Time::now();
    const int accepted=bounded([&]{return combine_tick_surface(now,x,y,authored_ground(x,y),surfaceLayer,1,&packet);});
    const double tickMs=std::chrono::duration<double,std::milli>(Time::now()-tickStart).count();
    if(tickMs>maximumTick)maximumTick=tickMs;
    if(!accepted)throw "surface riding tick refused";
    for(int i=0;i<4;i++)if(!std::isfinite(combine_value(i)))throw "surface actual Session pose nonfinite";
    Sleep(17);
}
static void surface_dismount() {
    combine_stop();
    if(std::isfinite(combine_value(0)))throw "surface dismounted pose remains available";
    Sleep(100);
    if(std::isfinite(combine_value(0)))throw "surface stale output after dismount";
}
static void surface_proof() {
    phase="ramp mount";surface_mount();phase="ramp ride";Packet neutral{},push{0x4000,{0,0},{0,0},{0,0}};
    for(int n=0;n<30;n++)surface_tick(neutral);
    const float startX=combine_value(0),startY=combine_value(1),startZ=combine_value(2);
    float minimumGround=authored_ground(startX,startY),maximumGround=minimumGround;
    for(int n=0;n<90;n++) {
        surface_tick(push);
        const float ground=authored_ground(combine_value(0),combine_value(1));
        if(ground<minimumGround)minimumGround=ground;
        if(ground>maximumGround)maximumGround=ground;
    }
    for(int n=0;n<30;n++)surface_tick(neutral);
    const float endX=combine_value(0),endY=combine_value(1),endZ=combine_value(2);
    const float groundChange=authored_ground(endX,endY)-authored_ground(startX,startY);
    if(std::hypot(endX-startX,endY-startY)<0.1f)throw "surface push has no measurable displacement";
    if(maximumGround-minimumGround<0.1f || std::fabs(groundChange)<0.1f)throw "surface ride did not cross distinct authored heights";
    if(std::fabs((endZ-startZ)-groundChange)>0.15f)throw "surface actual Session height failed to follow authored ramp";
    surface_dismount();
    std::puts("PASS: real Session mounted authored ramp, rode 90 push ticks across changing heights, followed ramp height and discarded dismounted output");
    for(int fault=0;fault<2;fault++) {
        phase="fault mount";surface_mount();phase="fault neutral tick";surface_tick(neutral);
        const float x=combine_value(0),y=combine_value(1);
        const uint32_t layer=fault?surfaceLayer+1:surfaceLayer,valid=fault?1:0;
        if(bounded([&]{return combine_tick_surface(GetTickCount(),x,y,authored_ground(x,y),layer,valid,&neutral);}))throw fault?"surface wrong layer accepted":"surface unavailable observation accepted";
        surface_dismount();
        phase="recovery mount";surface_mount();phase="recovery tick";surface_tick(neutral);surface_dismount();
    }
    std::puts("PASS: unavailable authored observation and wrong layer refuse riding; explicit stop clears pose and subsequent remount recovers");
}
int main(int argc,char** argv) {
    if(argc!=2 || (std::strcmp(argv[1],"--in-process")!=0 && std::strcmp(argv[1],"--worker")!=0)) {
        std::puts("FAIL: usage: native-surface [--in-process|--worker]");return 1;
    }
    workerBackend=std::strcmp(argv[1],"--worker")==0;
    std::printf("BACKEND: %s; expected initial preparation return %d\n",workerBackend?"worker":"in-process",workerBackend?2:1);
    const auto start=Time::now();
    try {
        surface_proof();
        std::printf("PASS: %s authored surface; maximum measured mount/poll/tick call %.3f ms; elapsed %.3f seconds\n",
            workerBackend?"worker":"in-process",maximum,std::chrono::duration<double>(Time::now()-start).count());
        return 0;
    } catch(const char* reason) {combine_stop();std::printf("FAIL: %s; phase %s; attempted ticks %u; maximum measured mount/poll/tick %.3f ms; max tick %.3f ms; max tick-start gap %lu ms\n",reason,phase,ticks,maximum,maximumTick,static_cast<unsigned long>(maximumGap));return 1;}
}
