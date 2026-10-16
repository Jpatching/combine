"""Exercise the plugin's actual readiness functions with deterministic Win32 inputs."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]


class ForegroundTests(unittest.TestCase):
    def test_input_readiness_preserves_focus_without_requiring_caption(self):
        source = (ROOT / 'tools/gtaiv-skate/plugin.cpp').read_text()
        functions = source.split('bool foreground_allowed() {', 1)[1].split('bool read_input(', 1)[0]
        harness = r'''
#include <atomic>
#include <iostream>
using DWORD = unsigned long;
constexpr int GWL_STYLE=-16, WS_CAPTION=0x00C00000, ERROR_SUCCESS=0;
int window=1, style=0, pad_result=1;
DWORD foreground_process=42;
bool minimized=false;
std::atomic<int> input_mode{1};
struct XINPUT_STATE {};
int GetForegroundWindow(){return window;}
void GetWindowThreadProcessId(int,DWORD* process){*process=foreground_process;}
DWORD GetCurrentProcessId(){return 42;}
bool IsIconic(int){return minimized;}
int GetWindowLong(int,int){return style;}
int GetAsyncKeyState(int){return 0;}
int XInputGetState(int,XINPUT_STATE*){return pad_result;}
'''+ 'bool foreground_allowed() {' + functions + r'''
int main(){
 int failures=0;
 auto check=[&](const char* name,bool expected){
  if(input_available()!=expected){std::cerr<<"FAIL: "<<name<<"\n";++failures;}
 };
 check("focused captionless keyboard input must be ready",true);
 style=WS_CAPTION;check("focused captioned keyboard input",true);
 style=0;foreground_process=99;check("other process refused",false);
 foreground_process=42;minimized=true;check("minimized refused",false);
 minimized=false;window=0;check("missing window refused",false);
 window=1;input_mode=0;check("disconnected controller refused",false);
 pad_result=ERROR_SUCCESS;check("focused captionless controller input",true);
 foreground_process=99;check("connected controller in other process refused",false);
 return failures?1:0;
}
'''
        with tempfile.TemporaryDirectory(prefix='combine-focus-') as directory:
            cpp = Path(directory) / 'focus.cpp'
            exe = Path(directory) / ('focus.exe' if sys.platform == 'win32' else 'focus')
            cpp.write_text(harness)
            subprocess.run(['g++', '-std=c++17', str(cpp), '-o', str(exe)], check=True)
            result = subprocess.run([str(exe)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
