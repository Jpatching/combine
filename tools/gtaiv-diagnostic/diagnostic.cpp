// SDK signatures: CLEO Redux bbf6773fe8cc1bfa95c73509a25928f97b0d8d13.
// Resolve only existing exports; no hooks, game offsets, setters or worker thread.
#include <windows.h>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

static_assert(sizeof(void*) == 4, "GTA IV requires an x86 plugin");
namespace {
using Context = void*;
using Handler = int (*)(Context); // SDK HandlerResult::CONTINUE = 0
using Tick = void (*)(unsigned int, int);
struct SDK {
    long (*version)();
    int (*host)(); // SDK HostId::IV = 9
    void (*log)(const char*);
    void (*command)(const char*, Handler, const char*);
    intptr_t (*integer)(Context);
    float (*number)(Context);
    void (*output)(Context, intptr_t);
    void (*after)(Tick);
} sdk{};
bool checked = false, ready = false;
unsigned int callback_time = 0;
int callback_step = 0;
uint64_t callbacks = 0, samples = 0;
DWORD callback_thread = 0;

template<typename T> bool bind(HMODULE module, const char* name, T& target) {
    auto address = GetProcAddress(module, name);
    static_assert(sizeof(address) == sizeof(target));
    std::memcpy(&target, &address, sizeof(target));
    return target != nullptr;
}

bool exact_version() {
    char path[MAX_PATH];
    const auto length = GetModuleFileNameA(nullptr, path, MAX_PATH);
    if (!length || length >= MAX_PATH) return false;
    DWORD unused = 0;
    const DWORD size = GetFileVersionInfoSizeA(path, &unused);
    if (!size || size > 1024 * 1024) return false;
    std::vector<unsigned char> data(size);
    if (!GetFileVersionInfoA(path, 0, size, data.data())) return false;
    VS_FIXEDFILEINFO* info = nullptr;
    UINT info_size = 0;
    if (!VerQueryValueA(data.data(), "\\", reinterpret_cast<void**>(&info), &info_size)
        || info_size < sizeof(VS_FIXEDFILEINFO) || info->dwSignature != 0xfeef04bd)
        return false;
    return info->dwFileVersionMS == 0x00010002 && info->dwFileVersionLS == 0x0000003b;
}

bool qualified_identity() {
    if (!checked) {
        checked = true;
        ready = sdk.version() >= 4 && sdk.host() == 9 && exact_version();
        char message[160];
        std::snprintf(message, sizeof(message),
            "COMBINE_IV identity sdk=%ld host=%d version_1_2_0_59=%d enabled=%d",
            sdk.version(), sdk.host(), exact_version(), ready);
        sdk.log(message);
    }
    return ready;
}

void after_scripts(unsigned int time, int step) {
    if (!qualified_identity()) return;
    callback_time = time;
    callback_step = step;
    callback_thread = GetCurrentThreadId();
    ++callbacks;
    if (callbacks == 1) sdk.log("COMBINE_IV first after-scripts callback");
}

int is_ready(Context context) {
    sdk.output(context, qualified_identity() && callbacks > 0 ? 1 : 0);
    return 0;
}

int sample(Context context) {
    // Consume all 17 arguments in definition order, including when disabled.
    const auto timer = sdk.integer(context);
    const float frame = sdk.number(context);
    const auto ped = sdk.integer(context), on_foot = sdk.integer(context);
    float values[9];
    for (auto& value : values) value = sdk.number(context);
    intptr_t axes[4];
    for (auto& axis : axes) axis = sdk.integer(context);
    if (!qualified_identity() || callbacks == 0) return 0;
    ++samples;
    if (samples != 1 && samples % 60 != 0) return 0;
    char message[768];
    std::snprintf(message, sizeof(message),
        "COMBINE_IV sample=%llu callbacks=%llu prior_callback_time=%u prior_callback_step=%d "
        "thread=%lu prior_callback_thread=%lu timer_ms=%ld frame_raw=%.9g ped=%ld on_foot=%ld "
        "position=(%.6g,%.6g,%.6g) camera=(%.6g,%.6g,%.6g) rotation_raw=(%.6g,%.6g,%.6g) "
        "sticks_raw=(%ld,%ld,%ld,%ld)",
        static_cast<unsigned long long>(samples), static_cast<unsigned long long>(callbacks),
        callback_time, callback_step, GetCurrentThreadId(), callback_thread,
        static_cast<long>(timer), frame, static_cast<long>(ped), static_cast<long>(on_foot),
        values[0], values[1], values[2], values[3], values[4], values[5],
        values[6], values[7], values[8], static_cast<long>(axes[0]),
        static_cast<long>(axes[1]), static_cast<long>(axes[2]), static_cast<long>(axes[3]));
    sdk.log(message);
    return 0;
}
} // namespace

BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, LPVOID) {
    if (reason != DLL_PROCESS_ATTACH) return TRUE;
    DisableThreadLibraryCalls(instance);
    const auto module = GetModuleHandleA("cleo_redux.asi");
    if (!module || !bind(module, "GetSDKVersion", sdk.version)
        || !bind(module, "GetHostId", sdk.host) || !bind(module, "Log", sdk.log)
        || !bind(module, "RegisterCommand", sdk.command)
        || !bind(module, "GetIntParam", sdk.integer) || !bind(module, "GetFloatParam", sdk.number)
        || !bind(module, "SetIntParam", sdk.output) || !bind(module, "OnAfterScripts", sdk.after))
        return FALSE;
    if (sdk.version() < 4) return FALSE;
    // CLEO documents registration in DllMain. Identity/file reads wait for callbacks.
    sdk.command("COMBINE_IV_READY", is_ready, nullptr);
    sdk.command("COMBINE_IV_SAMPLE", sample, nullptr);
    sdk.after(after_scripts);
    return TRUE;
}
