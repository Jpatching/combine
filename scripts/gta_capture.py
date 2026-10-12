"""Selected GTA-window recording with reviewed local capture tools; no uploads."""
import contextlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


class Capture:
    def __init__(self, folder):
        self.folder = folder
        guide = ROOT / '.private/tool-guides/universal-modder'
        pin = json.loads((ROOT / 'research/tool-guides.json').read_text())['universal-modder']['revision']
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=guide, text=True).strip()
        changed = subprocess.check_output(['git', 'status', '--porcelain'], cwd=guide, text=True).strip()
        if revision != pin or changed: raise ValueError('Reviewed capture guide changed')
        sys.path.insert(0, str(guide))
        os.environ['UM_HOME'] = str(ROOT / '.private/tooling/um-state')
        from um import win
        from um.common import to_win
        self.module = win; self.to_win = to_win
        self.ffmpeg = win.ffmpeg_win()
        self.recorder = win.Recorder(exe='GTAIV.exe', out=str(folder / 'trial'), audio=False, fps=30)
        self.original = win.to_posix
        owned = {self.recorder.base + suffix: str(folder / ('trial' + suffix))
                 for suffix in ('.mkv', '.json', '.ffmpeg.log')}
        win.to_posix = lambda value: owned.get(str(value), self.original(value))

    def start(self):
        with (self.folder / 'capture-private.log').open('w') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            self.recorder.start()

    def stop(self):
        try:
            with (self.folder / 'capture-stop-private.log').open('w') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                self.recorder.stop()
            if self.recorder.video: self.recorder.video.wait(timeout=5)
            source = self.folder / 'trial.mkv'; target = self.folder / 'trial.mp4'
            with (self.folder / 'remux-private.log').open('w') as log:
                subprocess.run([self.ffmpeg, '-nostdin', '-v', 'error', '-i', self.to_win(source),
                                '-map', '0:v:0', '-c', 'copy', '-movflags', '+faststart', self.to_win(target)],
                               stdout=log, stderr=log, timeout=30, check=True)
            probe = str(Path(self.ffmpeg).with_name('ffprobe.exe'))
            def count(path):
                p = subprocess.run([probe, '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                                    '-show_entries', 'stream=nb_read_frames', '-of', 'json', self.to_win(path)],
                                   text=True, capture_output=True, timeout=20, check=True)
                return int(json.loads(p.stdout)['streams'][0]['nb_read_frames'])
            frames = count(source)
            if frames <= 0 or count(target) != frames: raise ValueError('Video verification failed')
            return target
        finally:
            self.module.to_posix = self.original


def screenshot(path):
    from um.win import shot
    with path.with_suffix('.private.log').open('w') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        shot(str(path), exe='GTAIV.exe')
