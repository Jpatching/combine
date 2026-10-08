"""Add adapter commands to exact pinned GTA IV definitions into a new file."""
import argparse
import hashlib
import json
from pathlib import Path

BASE_SHA256 = "ba78c1ae32ea2eb800311f4513617e75c6283ac94805db016d157745356eb21b"
COMMANDS = {
    "READY": ([], "int"), "TOGGLE": ([], "int"), "STOP": ([], None),
    "VERTEX": ([("x","float"),("y","float"),("z","float")], "int"),
    "MOUNT": ([("x","float"),("y","float"),("ground","float"),
               ("heading","float"),("scale","float")], "int"),
    "TICK": ([("timer","int"),("ground","float"),("valid","int")], "int"),
    "VALUE": ([("index","int")], "float"),
    "CLAIM": ([("player","int"),("ped","int"),("camera","int")], None),
    "RELEASE": ([], None), "RESCUE": ([], "int"),
}

def prepare(source, destination):
    content=source.read_bytes()
    if hashlib.sha256(content).hexdigest()!=BASE_SHA256:
        raise ValueError("Definitions differ from pinned source")
    definitions=json.loads(content)
    commands=[]
    for suffix,(fields,result) in COMMANDS.items():
        commands.append({"name":"COMBINE_SKATE_"+suffix,
            "num_params":len(fields)+(result is not None),
            "input":[{"name":name,"type":kind} for name,kind in fields],
            "output":[{"name":"value","type":result}] if result else []})
    for command in commands:
        if command["name"]=="COMBINE_SKATE_RESCUE":
            command["output"]=[{"name":name,"type":"int"} for name in ("player","ped","camera")]
            command["num_params"]=3
    definitions["extensions"].append({"name":"combine_skate","commands":commands})
    with destination.open("x",encoding="utf-8") as output:
        json.dump(definitions,output,indent=2);output.write("\n")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path);parser.add_argument("destination",type=Path)
    args=parser.parse_args();prepare(args.source,args.destination)
