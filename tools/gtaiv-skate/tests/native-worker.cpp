// Standalone Windows parent ABI smoke. Never attaches to or controls GTA.
#include <windows.h>
#include <tlhelp32.h>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdint>
extern "C" {
struct Packet {uint16_t buttons;int16_t left[2],right[2];uint8_t triggers[2];};
int combine_config(const wchar_t*,uint32_t);void combine_stop();int combine_vertex(float,float,float);
int combine_mount(float,float,float,float,float);int combine_poll();int combine_tick(uint32_t,float,const Packet*);float combine_value(int);
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
int main() {
    try {
        wchar_t exe[32768];const auto length=GetModuleFileNameW(nullptr,exe,32768);
        if(!length || !combine_config(exe,length))throw "configuration refused";
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
