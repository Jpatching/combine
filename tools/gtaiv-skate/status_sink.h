// Fixed, asset-free state only; no coordinates, identities, settings or log text.
#pragma once
#include <windows.h>
#include <cstdio>
#include <string>

namespace combine_status {
inline unsigned long long unix_ms(FILETIME time) {
    ULARGE_INTEGER value{}; value.LowPart=time.dwLowDateTime; value.HighPart=time.dwHighDateTime;
    return value.QuadPart/10000ULL-11644473600000ULL;
}
inline bool publish(int scene, bool control, bool on_foot, bool ready, bool mounted, bool controller) {
    static DWORD last_tick=0;
    static int last_state=-1;
    const int state=scene|(control<<3)|(on_foot<<4)|(ready<<5)|(mounted<<6)|(controller<<7);
    const DWORD tick=GetTickCount();
    if(state==last_state && tick-last_tick<500)return true;
    wchar_t directory[32768];
    const DWORD length=GetEnvironmentVariableW(L"LOCALAPPDATA",directory,32768);
    if(!length || length>=32768)return false;
    std::wstring folder=std::wstring(directory)+L"\\Combine";
    const auto safe_directory=[](const std::wstring& path) {
        if(!CreateDirectoryW(path.c_str(),nullptr) && GetLastError()!=ERROR_ALREADY_EXISTS)return false;
        const DWORD attributes=GetFileAttributesW(path.c_str());
        return attributes!=INVALID_FILE_ATTRIBUTES && (attributes&FILE_ATTRIBUTE_DIRECTORY)
            && !(attributes&FILE_ATTRIBUTE_REPARSE_POINT);
    };
    if(!safe_directory(folder))return false;
    folder+=L"\\gtaiv-status";
    if(!safe_directory(folder))return false;
    // A separate PID-specific temporary file avoids partially read snapshots.
    const std::wstring temporary=folder+L"\\state-"+std::to_wstring(GetCurrentProcessId())+L".tmp";
    const DWORD old=GetFileAttributesW(temporary.c_str());
    if(old!=INVALID_FILE_ATTRIBUTES && (old&FILE_ATTRIBUTE_REPARSE_POINT))return false;
    FILETIME created{},exit{},kernel{},user{},now{};
    if(!GetProcessTimes(GetCurrentProcess(),&created,&exit,&kernel,&user))return false;
    GetSystemTimeAsFileTime(&now);
    const char* scenes[]={"unknown","gameplay","cutscene","paused","unavailable"};
    if(scene<0 || scene>4)return false;
    char data[512];
    const int size=std::snprintf(data,sizeof(data),
        "{\"schema\":1,\"pid\":%lu,\"process_start_ms\":%llu,\"updated_ms\":%llu,"
        "\"scene\":\"%s\",\"player_control\":%s,\"on_foot\":%s,\"adapter_ready\":%s,"
        "\"mounted\":%s,\"controller\":%s}\n",
        GetCurrentProcessId(),unix_ms(created),unix_ms(now),scenes[scene],
        control?"true":"false",on_foot?"true":"false",ready?"true":"false",
        mounted?"true":"false",controller?"true":"false");
    if(size<=0 || size>=static_cast<int>(sizeof(data)))return false;
    HANDLE file=CreateFileW(temporary.c_str(),GENERIC_WRITE,0,nullptr,CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL|FILE_FLAG_OPEN_REPARSE_POINT,nullptr);
    if(file==INVALID_HANDLE_VALUE)return false;
    DWORD written=0;
    const bool complete=WriteFile(file,data,static_cast<DWORD>(size),&written,nullptr)
        && written==static_cast<DWORD>(size);
    CloseHandle(file);
    const std::wstring destination=folder+L"\\state.json";
    const bool saved=complete && MoveFileExW(temporary.c_str(),destination.c_str(),MOVEFILE_REPLACE_EXISTING);
    if(!saved){DeleteFileW(temporary.c_str());return false;}
    last_tick=tick;last_state=state;return true;
}
}
