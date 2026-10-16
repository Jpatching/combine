// Standalone Windows parent ABI smoke. Never attaches to or controls GTA.
#include <windows.h>
#include <tlhelp32.h>
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
template<class F> int bounded(F action) {const auto start=Time::now();const int result=action();const double ms=std::chrono::duration<double,std::milli>(Time::now()-start).count();if(ms>maximum)maximum=ms;if(ms>50)throw "blocking parent call";return result;}
static void mount(float originX=100.f,float originY=200.f) {
    combine_stop();Sleep(100);
    for(int y=0;y<5;y++)for(int x=0;x<5;x++)if(!combine_vertex(originX+(x-2)*2,originY+(y-2)*2,10.f))throw "vertex refusal";
    if(bounded([&]{return combine_mount(originX,originY,10,0,1);})!=2)throw "prepare refused";
    const auto start=Time::now();int state=2;
    while(state==2 && Time::now()-start<std::chrono::seconds(60)) {state=bounded([]{return combine_poll();});Sleep(5);}
    if(state!=1)throw "preparation unavailable";
    std::printf("PASS: asynchronous prepare; elapsed %.3f seconds\n",std::chrono::duration<double>(Time::now()-start).count());
}
static DWORD owned_worker() {
    const HANDLE snapshot=CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0);PROCESSENTRY32W entry{};entry.dwSize=sizeof(entry);DWORD id=0;
    if(Process32FirstW(snapshot,&entry))do {if(entry.th32ParentProcessID==GetCurrentProcessId() && _wcsicmp(entry.szExeFile,L"combine_skate_worker.exe")==0) {id=entry.th32ProcessID;break;}}while(Process32NextW(snapshot,&entry));
    CloseHandle(snapshot);if(!id)throw "owned worker missing";return id;
}
static void stall_owned() {
    const DWORD id=owned_worker();const HANDLE snapshot=CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);THREADENTRY32 entry{};entry.dwSize=sizeof(entry);int count=0;
    if(Thread32First(snapshot,&entry))do {if(entry.th32OwnerProcessID==id) {const HANDLE thread=OpenThread(THREAD_SUSPEND_RESUME,FALSE,entry.th32ThreadID);if(thread) {if(SuspendThread(thread)!=DWORD(-1))count++;CloseHandle(thread);}}}while(Thread32Next(snapshot,&entry));
    CloseHandle(snapshot);if(!count)throw "owned worker stall unavailable";
}
static void drive(uint16_t buttons,int16_t stick) {
    Packet p{buttons,{stick,0},{0,0},{0,0}};
    for(int n=0;n<30;n++) {if(!bounded([&]{return combine_tick(GetTickCount(),10,&p);}))throw "tick refused";for(int i=0;i<4;i++)if(!std::isfinite(combine_value(i)))throw "invalid pose";Sleep(17);}
}
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
    combine_stop();Sleep(100);
    surface_upload();
    if(bounded([]{return combine_mount_surface(100,200,10,0,1,surfaceLayer,1);})!=2)throw "surface preparation refused";
    const auto start=Time::now();int state=2;
    while(state==2 && Time::now()-start<std::chrono::seconds(60)) {state=bounded([]{return combine_poll();});Sleep(5);}
    if(state!=1)throw "surface asynchronous preparation unavailable";
}
static void surface_tick(const Packet& packet) {
    const float x=combine_value(0),y=combine_value(1);
    if(!std::isfinite(x)||!std::isfinite(y))throw "surface query pose unavailable";
    if(!bounded([&]{return combine_tick_surface(GetTickCount(),x,y,authored_ground(x,y),surfaceLayer,1,&packet);}))throw "surface riding tick refused";
    for(int i=0;i<4;i++)if(!std::isfinite(combine_value(i)))throw "surface actual Session pose nonfinite";
    Sleep(17);
}
static void surface_dismount() {
    combine_stop();
    if(std::isfinite(combine_value(0)))throw "surface dismounted pose remains available";
    Sleep(100);
    if(std::isfinite(combine_value(0)))throw "surface stale output after dismount";
}
static void surface_cancel_proof() {
    Packet neutral{};
    // A preceding stop retained an idle warm child. Suspend only that owned child;
    // a 4096-triangle frame exceeds its pipe buffer and cannot drain while stalled.
    const DWORD waitingPid=owned_worker();
    const HANDLE waiting=OpenProcess(SYNCHRONIZE,FALSE,waitingPid);
    if(!waiting)throw "surface cancelled writer process wait unavailable";
    DWORD exited=WAIT_FAILED;
    try {
        stall_owned();surface_upload(4096);
        if(bounded([]{return combine_mount_surface(100,200,10,0,1,surfaceLayer,1);})!=2)throw "surface large asynchronous preparation refused";
        Sleep(100);
        if(WaitForSingleObject(waiting,0)!=WAIT_TIMEOUT)throw "surface stalled child exited before explicit cancellation";
        bounded([]{combine_stop();return 0;});
        exited=WaitForSingleObject(waiting,2000);
    } catch(...) {CloseHandle(waiting);throw;}
    CloseHandle(waiting);
    if(exited!=WAIT_OBJECT_0)throw "surface cancellation did not terminate stalled owned child within 2 seconds";
    if(std::isfinite(combine_value(0)))throw "surface cancelled large preparation retained pose";
    surface_mount();surface_tick(neutral);surface_dismount();
    std::puts("PASS: cancelled large geometry preparation with suspended owned child, observed child exit and recovered with fresh Session");
}
static void surface_proof() {
    surface_mount();Packet neutral{},push{0x4000,{0,0},{0,0},{0,0}};
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
        surface_mount();surface_tick(neutral);
        const float x=combine_value(0),y=combine_value(1);
        const uint32_t layer=fault?surfaceLayer+1:surfaceLayer,valid=fault?1:0;
        if(bounded([&]{return combine_tick_surface(GetTickCount(),x,y,authored_ground(x,y),layer,valid,&neutral);}))throw fault?"surface wrong layer accepted":"surface unavailable observation accepted";
        surface_dismount();
        surface_mount();surface_tick(neutral);surface_dismount();
    }
    std::puts("PASS: unavailable authored observation and wrong layer refuse riding; explicit stop clears pose and subsequent remount recovers");
    surface_cancel_proof();
}
int main(int argc,char** argv) {
    try {
        wchar_t exe[32768];const auto length=GetModuleFileNameW(nullptr,exe,32768);
        if(!length || !combine_config(exe,length))throw "configuration refused";
        if(argc==2 && std::strcmp(argv[1],"--surface-only")==0) {
            surface_proof();std::printf("PASS: surface-only maximum parent call %.3f ms\n",maximum);return 0;
        }
        if(argc==2 && std::strcmp(argv[1],"--surface-cancel-only")==0) {
            surface_mount();surface_dismount();surface_cancel_proof();return 0;
        }
        if(argc!=1)throw "usage: native-worker [--surface-only|--surface-cancel-only]";
        mount();drive(0,0);const DWORD warmPid=owned_worker();const float neutralX=combine_value(0),neutralY=combine_value(1);combine_stop();
        if(std::isfinite(combine_value(0)))throw "dismounted pose remains available";
        Sleep(100);
        if(std::isfinite(combine_value(0)))throw "stale output after dismount";
        mount();if(owned_worker()!=warmPid)throw "warm Session process replaced";drive(0x4000,0);const float pushX=combine_value(0),pushY=combine_value(1),pushHeading=combine_value(3);combine_stop();
        if(std::hypot(pushX-neutralX,pushY-neutralY)<0.001)throw "push motion unchanged";
        mount();drive(0x4000,16000);if(std::fabs(combine_value(3)-pushHeading)<0.001)throw "steering unchanged";combine_stop();
        mount(102,202);if(std::fabs(combine_value(0)-102)>0.5 || std::fabs(combine_value(1)-202)>0.5)throw "collision revision origin unchanged";
        combine_stop();
        std::puts("PASS: real Session push/steer, same-child warm remount, collision revision and stale pose discard");
        mount();stall_owned();Packet p{};const auto start=Time::now();bool refused=false;
        while(Time::now()-start<std::chrono::seconds(2)) {if(!bounded([&]{return combine_tick(GetTickCount(),10,&p);})) {refused=true;break;}Sleep(5);}
        if(!refused || Time::now()-start>std::chrono::milliseconds(500))throw "stall detection exceeded bound";
        combine_stop();std::puts("PASS: owned worker stall refuses riding; GTA native restoration requires live test");
        mount();const HANDLE process=OpenProcess(PROCESS_TERMINATE,FALSE,owned_worker());if(!process)throw "owned exit unavailable";TerminateProcess(process,3);CloseHandle(process);
        refused=false;const auto exited=Time::now();
        while(Time::now()-exited<std::chrono::seconds(2)) {if(!bounded([&]{return combine_tick(GetTickCount(),10,&p);})) {refused=true;break;}Sleep(5);}
        if(!refused)throw "worker exit not detected";
        combine_stop();mount();drive(0,0);combine_stop();
        std::printf("PASS: exit detected and fresh worker remount; maximum parent call %.3f ms\n",maximum);return 0;
    } catch(const char* reason) {combine_stop();std::printf("FAIL: %s\n",reason);return 1;}
}
