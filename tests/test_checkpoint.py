"""Strict checkpoint preparation through the public command; authored points only."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CheckpointTests(unittest.TestCase):
    def test_authored_checkpoint_native_boundary_moves_once_and_refuses_owned_or_paused_game(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory); point = folder / 'point.json'; script = folder / 'checkpoint.js'
            point.write_text(json.dumps({'label': 'authored', 'position': [10, 20, 3]}))
            subprocess.run([sys.executable, str(ROOT / 'scripts/evidence_hub.py'), '--state', str(folder / 'state'),
                'checkpoint', '--point', str(point), '--output', str(script)], check=True, capture_output=True)
            harness = folder / 'fixture.cjs'
            harness.write_text('''const fs=require('fs'),vm=require('vm');
let ticks=0,moves=0,position={x:0,y:0,z:1},events=[];
const mode=process.argv[3],stop=new Error('fixture-end');
const context={Date:{now:()=>ticks*100},log:line=>events.push(JSON.parse(line.split(' PRIVATE ')[1])),
 wait:()=>{if(++ticks>150)throw stop;},native:(name,...args)=>{
 if(name==='COMBINE_SKATE_EVAL_KEY')return ticks===1&&args[0]===2?1:0;
 if(name==='COMBINE_SKATE_EVAL_OWNER')return {player:mode==='mounted'?0:-1};
 if(name==='GET_PLAYER_ID'||name==='CONVERT_INT_TO_PLAYERINDEX')return 0;
 if(name==='GET_PLAYER_CHAR')return 7;
 if(name==='GET_CHAR_COORDINATES')return {...position};
 if(name==='SET_CHAR_COORDINATES_NO_OFFSET'){moves++;position={x:args[1],y:args[2],z:args[3]};return;}
 if(name==='REQUEST_COLLISION_AT_POSN')return;
 if(name==='IS_PAUSE_MENU_ACTIVE')return mode==='paused';
 if(name==='HAS_CUTSCENE_LOADED'||name==='IS_CHAR_IN_AIR'||name==='IS_CHAR_DEAD')return false;
 if(name==='IS_CHAR_WAITING_FOR_WORLD_COLLISION')return mode==='unavailable';
 if(['COMBINE_SKATE_READY','IS_PLAYER_PLAYING','DOES_CHAR_EXIST','IS_CHAR_ON_FOOT','IS_PLAYER_CONTROL_ON'].includes(name))return true;
 throw new Error('Unknown native '+name);
}};
try{vm.runInNewContext(fs.readFileSync(process.argv[2],'utf8'),context);}catch(e){if(e!==stop)throw e;}
console.log(JSON.stringify({moves,position,events}));''')
            def run(mode):
                result = subprocess.run(['node', str(harness), str(script), mode], text=True, capture_output=True, check=True)
                return json.loads(result.stdout)
            success = run('ready')
            self.assertEqual(success['moves'], 1)
            self.assertEqual(success['events'][0]['event'], 'reached')
            for mode in ('mounted','paused'):
                self.assertEqual(run(mode)['moves'], 0)
            refused = run('unavailable')
            self.assertEqual(refused['position'], {'x': 0, 'y': 0, 'z': 1})
            self.assertEqual(refused['events'][0]['event'], 'restored')

    def test_checkpoint_preparation_is_strict_data_and_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); point = root / 'point.json'; output = root / 'checkpoint.js'
            point.write_text(json.dumps({'label': 'authored', 'position': [10, 20, 3]}))
            command = [sys.executable, str(ROOT / 'scripts/evidence_hub.py'), '--state', str(root / 'state'),
                       'checkpoint', '--point', str(point), '--output', str(output)]
            result = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            original = output.read_bytes()
            self.assertIn(b'COMBINE_SKATE_EVAL_KEY', original)
            self.assertIn(b'loading/layer remain unqualified', original)
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), original)
            for value in [{'label': 'bad', 'position': [1, 2, float('nan')]},
                          {'label': 'bad', 'position': [1, 2, 3], 'command': 'shell'}]:
                point.write_text(json.dumps(value)); output.unlink(missing_ok=True)
                self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
                self.assertFalse(output.exists())


if __name__ == '__main__': unittest.main()
