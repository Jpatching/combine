// CLEO Redux SDK bbf6773fe8cc1bfa95c73509a25928f97b0d8d13.
// GTA natives stay in JS. The optional worker runs Session outside GTA.
#include <windows.h>
#include <xinput.h>
#include <cstdint>
#include <cstring>
#include <vector>
#include <atomic>
#include "status_sink.h"
static_assert(sizeof(void*)==4,"GTA IV is x86");
extern "C" {
struct Packet {uint16_t buttons; int16_t left[2],right[2]; uint8_t triggers[2];};
int combine_config(const wchar_t*,uint32_t);
int combine_poll();void combine_reset();
void combine_stop(); int combine_vertex(float,float,float);
int combine_mount(float,float,float,float,float);
int combine_tick(uint32_t,float,const Packet*); float combine_value(int);
}
namespace {
using Context=void*; using Handler=int(*)(Context);
struct SDK {
    long(*version)(); int(*host)(); void(*log)(const char*);
    void(*command)(const char*,Handler,const char*);
    intptr_t(*integer)(Context); float(*number)(Context);
    void(*output_int)(Context,intptr_t); void(*output_float)(Context,float);
    void(*after)(void(*)(unsigned int,int)); void(*runtime_init)(void(*)());
} sdk{};
HINSTANCE plugin_instance=nullptr;
std::atomic<DWORD> script_thread{0}; bool enabled=false, key_held=false;
INIT_ONCE identity_once=INIT_ONCE_STATIC_INIT;
std::atomic<bool> callback_seen{false};
SRWLOCK ownership_lock=SRWLOCK_INIT;
DWORD heartbeat=0; bool owned=false, reset_pending=false; intptr_t owner[3]{};
template<class T> bool bind(HMODULE module,const char* name,T&target) {
    auto address=GetProcAddress(module,name); std::memcpy(&target,&address,sizeof(target)); return target!=nullptr;
}
BOOL CALLBACK check_identity(PINIT_ONCE,PVOID,PVOID*) {
    char path[MAX_PATH]; const auto length=GetModuleFileNameA(nullptr,path,MAX_PATH);
    if (!length||length>=MAX_PATH) return TRUE;
    DWORD unused=0; const auto size=GetFileVersionInfoSizeA(path,&unused);
    if (!size||size>1024*1024) return TRUE;
    std::vector<unsigned char> data(size); VS_FIXEDFILEINFO* info=nullptr; UINT info_size=0;
    if (!GetFileVersionInfoA(path,0,size,data.data())
        || !VerQueryValueA(data.data(),"\\",reinterpret_cast<void**>(&info),&info_size)
        || info_size<sizeof(*info)) return TRUE;
    enabled=sdk.host()==9 && info->dwSignature==0xfeef04bd
        && info->dwFileVersionMS==0x00010002 && info->dwFileVersionLS==0x0000003b;
    sdk.log(enabled?"COMBINE_SKATE identity ready; gameplay unverified":"COMBINE_SKATE identity rejected");
    return TRUE;
}
bool identity() {InitOnceExecuteOnce(&identity_once,check_identity,nullptr,nullptr);return enabled;}
void after(unsigned int,int) {if(identity()) callback_seen.store(true);}
bool on_thread() {
    const auto current=GetCurrentThreadId();
    return current==script_thread.load() && identity() && callback_seen.load();
}
void reset() {combine_reset();AcquireSRWLockExclusive(&ownership_lock);reset_pending=true;script_thread.store(0);ReleaseSRWLockExclusive(&ownership_lock);}
int claim(Context c) {
    intptr_t saved[3];for(auto &v:saved)v=sdk.integer(c);
    AcquireSRWLockExclusive(&ownership_lock);
    for(int i=0;i<3;++i)owner[i]=saved[i];
    owned=true;reset_pending=false;heartbeat=GetTickCount();
    ReleaseSRWLockExclusive(&ownership_lock);return 0;
}
int release(Context) {
    AcquireSRWLockExclusive(&ownership_lock);owned=false;reset_pending=false;
    ReleaseSRWLockExclusive(&ownership_lock);return 0;
}
int rescue(Context c) {
    intptr_t saved[3];
    AcquireSRWLockExclusive(&ownership_lock);
    const bool pending=owned&&(reset_pending||GetTickCount()-heartbeat>2000);
    for(int i=0;i<3;++i)saved[i]=pending?owner[i]:-1;
    if(pending) {reset_pending=true;combine_reset();}
    ReleaseSRWLockExclusive(&ownership_lock);
    for(auto v:saved)sdk.output_int(c,v);
    return 0;
}
int ready(Context c) {sdk.output_int(c,identity() && callback_seen.load() ? 1:0);return 0;}
int status(Context c) {
    const auto scene=static_cast<int>(sdk.integer(c));
    const bool control=sdk.integer(c)!=0, on_foot=sdk.integer(c)!=0;
    AcquireSRWLockShared(&ownership_lock);
    const bool mounted=owned;
    ReleaseSRWLockShared(&ownership_lock);
    XINPUT_STATE input{};
    combine_status::publish(scene,control,on_foot,identity()&&callback_seen.load(),mounted,
        XInputGetState(0,&input)==ERROR_SUCCESS);
    return 0;
}
int toggle(Context c) {
    const bool held=(GetAsyncKeyState(VK_F6)&0x8000)!=0;
    const bool rising=held&&!key_held; key_held=held;
    DWORD process=0;GetWindowThreadProcessId(GetForegroundWindow(),&process);
    const bool foreground=process==GetCurrentProcessId();
    sdk.output_int(c,rising&&foreground?1:0); return 0;
}
int stop(Context) {if(on_thread()) combine_stop();return 0;}
int vertex(Context c) {
    const float x=sdk.number(c),y=sdk.number(c),z=sdk.number(c);
    DWORD empty=0;script_thread.compare_exchange_strong(empty,GetCurrentThreadId());
    sdk.output_int(c,on_thread()?combine_vertex(x,y,z):0);return 0;
}
int mount(Context c) {
    const float x=sdk.number(c),y=sdk.number(c),z=sdk.number(c),heading=sdk.number(c),scale=sdk.number(c);
    XINPUT_STATE state{};
    const bool input=XInputGetState(0,&state)==ERROR_SUCCESS;
    wchar_t path[32768];const auto length=GetModuleFileNameW(plugin_instance,path,32768);
    const bool configured=on_thread()&&length>0&&length<32768&&combine_config(path,length);
    const auto ok=configured&&input?combine_mount(x,y,z,heading,scale):0;
    sdk.log(ok==2?"COMBINE_SKATE preparation submitted":ok==1?"COMBINE_SKATE mounted actual Session":"COMBINE_SKATE initialization rejected");
    sdk.output_int(c,ok);return 0;
}
int tick(Context c) {
    const auto timer=static_cast<uint32_t>(sdk.integer(c)); const float ground=sdk.number(c);
    const bool valid=sdk.integer(c)!=0;
    AcquireSRWLockExclusive(&ownership_lock);
    heartbeat=GetTickCount();const bool reset_requested=reset_pending||!owned;
    ReleaseSRWLockExclusive(&ownership_lock);
    XINPUT_STATE state{}; int ok=0;
    if(on_thread() && !reset_requested && valid && XInputGetState(0,&state)==ERROR_SUCCESS) {
        Packet p{state.Gamepad.wButtons,{state.Gamepad.sThumbLX,state.Gamepad.sThumbLY},
            {state.Gamepad.sThumbRX,state.Gamepad.sThumbRY},{state.Gamepad.bLeftTrigger,state.Gamepad.bRightTrigger}};
        ok=combine_tick(timer,ground,&p);
    } else if(on_thread()) combine_stop();
    sdk.output_int(c,ok);return 0;
}
int poll(Context c) {
    XINPUT_STATE state{};
    sdk.output_int(c,on_thread()&&XInputGetState(0,&state)==ERROR_SUCCESS?combine_poll():0);
    return 0;
}
int value(Context c) {const auto i=static_cast<int>(sdk.integer(c));sdk.output_float(c,on_thread()?combine_value(i):0.f);return 0;}
}
BOOL WINAPI DllMain(HINSTANCE instance,DWORD reason,LPVOID) {
    if(reason!=DLL_PROCESS_ATTACH)return TRUE;
    DisableThreadLibraryCalls(instance);plugin_instance=instance;
    const auto module=GetModuleHandleA("cleo_redux.asi");
    if(!module||!bind(module,"GetSDKVersion",sdk.version)||!bind(module,"GetHostId",sdk.host)
       ||!bind(module,"Log",sdk.log)||!bind(module,"RegisterCommand",sdk.command)
       ||!bind(module,"GetIntParam",sdk.integer)||!bind(module,"GetFloatParam",sdk.number)
       ||!bind(module,"SetIntParam",sdk.output_int)||!bind(module,"SetFloatParam",sdk.output_float)
       ||!bind(module,"OnAfterScripts",sdk.after)||!bind(module,"OnRuntimeInit",sdk.runtime_init)||sdk.version()<4)return FALSE;
    sdk.command("COMBINE_SKATE_READY",ready,nullptr);sdk.command("COMBINE_SKATE_TOGGLE",toggle,nullptr);
    sdk.command("COMBINE_SKATE_STOP",stop,nullptr);sdk.command("COMBINE_SKATE_VERTEX",vertex,nullptr);
    sdk.command("COMBINE_SKATE_MOUNT",mount,nullptr);sdk.command("COMBINE_SKATE_TICK",tick,nullptr);
    sdk.command("COMBINE_SKATE_VALUE",value,nullptr);
    sdk.command("COMBINE_SKATE_POLL",poll,nullptr);
    sdk.command("COMBINE_SKATE_CLAIM",claim,nullptr);sdk.command("COMBINE_SKATE_RELEASE",release,nullptr);
    sdk.command("COMBINE_SKATE_RESCUE",rescue,nullptr);
    sdk.command("COMBINE_GAME_STATUS",status,nullptr);
    sdk.after(after);sdk.runtime_init(reset);return TRUE;
}
