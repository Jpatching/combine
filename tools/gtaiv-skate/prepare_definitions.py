"""Prepare pinned GTA IV definitions with verified compatibility corrections."""
import argparse
import hashlib
import json
from pathlib import Path

BASE_SHA256 = "ba78c1ae32ea2eb800311f4513617e75c6283ac94805db016d157745356eb21b"
COMMANDS = {
    "POLL": ([], "int"), "READY": ([], "int"), "TOGGLE": ([], "int"), "STOP": ([], None),
    "VERTEX": ([("x","float"),("y","float"),("z","float")], "int"),
    "MOUNT": ([("x","float"),("y","float"),("ground","float"),
               ("heading","float"),("scale","float")], "int"),
    "TICK": ([("timer","int"),("ground","float"),("valid","int")], "int"),
    "VALUE": ([("index","int")], "float"),
    "CLAIM": ([("player","int"),("ped","int"),("camera","int")], None),
    "RELEASE": ([], None), "RESCUE": ([], "int"),
}

def prepare(source, destination, evaluation=False):
    content=source.read_bytes()
    if hashlib.sha256(content).hexdigest()!=BASE_SHA256:
        raise ValueError("Definitions differ from pinned source")
    definitions=json.loads(content)
    # GTA IV returns a success flag as well as writing the ground-height output.
    # Without this flag CLEO 1.5.1 reads success bits (1) as the float height.
    # Keep the pinned input intact; correct only the generated runtime definition.
    ground=next(command for extension in definitions["extensions"]
        for command in extension["commands"]
        if command["name"]=="GET_GROUND_Z_FOR_3D_COORD")
    ground.setdefault("attrs",{})["is_condition"]=True
    # DESTROY_CAM takes a camera handle by value. The pinned pointer annotation
    # makes CLEO pass its address, leaving the owned camera alive after dismount.
    destroy=next(command for extension in definitions["extensions"]
        for command in extension["commands"] if command["name"]=="DESTROY_CAM")
    destroy["input"][0]["source"]="any"
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
    commands.append({"name":"COMBINE_GAME_STATUS","num_params":3,
        "input":[{"name":name,"type":"int"} for name in ("scene","control","onFoot")],
        "output":[]})
    if evaluation:
        commands.extend([
            {"name":"COMBINE_SKATE_EVAL_INPUT","num_params":3,
             "input":[{"name":"profile","type":"int"},{"name":"duration","type":"int"}],
             "output":[{"name":"accepted","type":"int"}]},
            {"name":"COMBINE_SKATE_EVAL_OWNER","num_params":3,"input":[],
             "output":[{"name":name,"type":"int"} for name in ("player","ped","camera")]},
            {"name":"COMBINE_SKATE_EVAL_TIME","num_params":1,"input":[],
             "output":[{"name":"milliseconds","type":"int"}]},
            {"name":"COMBINE_SKATE_EVAL_KEY","num_params":2,
             "input":[{"name":"action","type":"int"}],
             "output":[{"name":"held","type":"int"}]},
        ])
    definitions["extensions"].append({"name":"combine_skate","commands":commands})
    with destination.open("x",encoding="utf-8") as output:
        json.dump(definitions,output,indent=2);output.write("\n")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path);parser.add_argument("destination",type=Path)
    parser.add_argument("--evaluation",action="store_true",help="Definitions for the explicitly opted-in evaluation plugin")
    args=parser.parse_args();prepare(args.source,args.destination,args.evaluation)
