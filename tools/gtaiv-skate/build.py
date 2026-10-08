"""Export pinned source and build an isolated x86 plugin; never installs or launches."""
import argparse
import io
from pathlib import Path
import shutil
import subprocess
import tarfile

PIN="f608f85e407ff1b7689d54a9aafdd16e95711ac4"
HERE=Path(__file__).resolve().parent

def build(source, destination, compiler, offline=True, worker=False):
    # Exact object export ignores unrelated upstream working-tree modifications.
    destination.mkdir(parents=True,exist_ok=False)
    archive=subprocess.run(["git","-C",str(source),"archive",PIN],check=True,capture_output=True).stdout
    upstream=destination/"upstream";upstream.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive)) as data:
        data.extractall(upstream,filter="data")
    adapter=destination/"adapter"
    shutil.copytree(HERE,adapter,ignore=shutil.ignore_patterns("__pycache__","target"))
    command=["cargo","build","--locked","--manifest-path",str(adapter/"Cargo.toml"),"--target","i686-pc-windows-gnu"]
    if worker:command.extend(["--features","worker","--release"])
    if offline:command.append("--offline")
    subprocess.run(command,check=True)
    profile="release" if worker else "debug"
    library=adapter/"target/i686-pc-windows-gnu"/profile/"libcombine_gtaiv_skate.a"
    if worker:shutil.copy2(adapter/"target/i686-pc-windows-gnu/release/combine_skate_worker.exe",destination/"combine_skate_worker.exe")
    subprocess.run([compiler,"-std=c++17","-shared","-static","-static-libgcc","-static-libstdc++",
        "-Wall","-Wextra","-Werror","-Wl,--exclude-all-symbols",str(HERE/"plugin.cpp"),str(library),
        "-o",str(destination/"combine_skate.cleo"),"-lversion","-lxinput","-lws2_32",
        "-lbcrypt","-luserenv","-lntdll"],check=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path);parser.add_argument("destination",type=Path)
    parser.add_argument("--compiler",default="i686-w64-mingw32-g++")
    parser.add_argument("--worker",action="store_true",help="Build optional asynchronous separate worker candidate")
    args=parser.parse_args();build(args.source.resolve(),args.destination.resolve(),args.compiler,worker=args.worker)
