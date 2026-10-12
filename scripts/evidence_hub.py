#!/usr/bin/env python3
"""Private candidate review and predefined GTA diagnostic requests."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import secrets
import sys
from urllib.parse import urlsplit

from evidence_store import Store

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'tools/workbench/hub.html'


def serve(store, port, origin=None, owner=None):
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Private requests and identities never enter terminal logs.

        def authenticated(self):
            host = self.headers.get('Host', '')
            allowed = urlsplit(origin).netloc if origin else f'127.0.0.1:{self.server.server_port}'
            if host != allowed:
                return False
            if owner and self.headers.get('Tailscale-User-Login', '').casefold() != owner.casefold():
                return False
            return True

        def send(self, code, body=b'', kind='application/json', extra=None):
            self.send_response(code)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            for key, value in (extra or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if not self.authenticated():
                self.send(403); return
            try:
                route = urlsplit(self.path).path
                static = {'/': PAGE, '/hub.js': PAGE.with_suffix('.js'), '/hub.css': PAGE.with_suffix('.css')}
                if route in static:
                    path = static[route]
                    self.send(200, path.read_bytes(), mimetypes.guess_type(path)[0]); return
                if route == '/api/state':
                    state = store.snapshot(); state['token'] = token
                    self.send(200, json.dumps(state).encode()); return
                if route.startswith('/media/'):
                    path = store.media(route.removeprefix('/media/'))
                    size = path.stat().st_size; start = 0; end = size - 1; code = 200
                    headers = {'Accept-Ranges': 'bytes'}
                    if 'Range' in self.headers:
                        match = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers['Range'])
                        if not match or not any(match.groups()):
                            self.send(416, extra={'Content-Range': f'bytes */{size}'}); return
                        a, b = match.groups()
                        start = int(a) if a else max(0, size - int(b))
                        end = min(int(b), end) if a and b else end
                        if start > end or start >= size:
                            self.send(416, extra={'Content-Range': f'bytes */{size}'}); return
                        code = 206; headers['Content-Range'] = f'bytes {start}-{end}/{size}'
                    self.send_response(code)
                    self.send_header('Content-Type', mimetypes.guess_type(path)[0] or 'application/octet-stream')
                    self.send_header('Content-Length', str(end - start + 1))
                    self.send_header('Cache-Control', 'private, no-store')
                    self.send_header('X-Content-Type-Options', 'nosniff')
                    for key, value in headers.items(): self.send_header(key, value)
                    self.end_headers()
                    with path.open('rb') as stream:
                        stream.seek(start); remaining = end - start + 1
                        while remaining:
                            data = stream.read(min(remaining, 64 * 1024))
                            if not data: break
                            self.wfile.write(data); remaining -= len(data)
                    return
                self.send(404)
            except FileNotFoundError:
                self.send(404)
            except (ValueError, OSError):
                self.send(409)

        def do_POST(self):
            expected_origin = origin or f'http://127.0.0.1:{self.server.server_port}'
            if (not self.authenticated() or self.headers.get('Origin') != expected_origin
                    or not secrets.compare_digest(self.headers.get('X-Combine-Token', ''), token)):
                self.send(403); return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 2048 or self.headers.get_content_type() != 'application/json':
                    raise ValueError('Invalid request body')
                value = json.loads(self.rfile.read(length))
                if not isinstance(value, dict): raise ValueError('Expected request object')
                if self.path == '/api/requests':
                    result = store.request(value)
                elif self.path == '/api/stop' and set(value) == {'id'}:
                    result = store.stop(value['id'])
                else:
                    self.send(404); return
                self.send(200, json.dumps(result).encode())
            except (ValueError, TypeError, KeyError):
                self.send(400, b'{"error":"Invalid predefined request"}')

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(f'http://127.0.0.1:{server.server_port}', flush=True)
    try: server.serve_forever()
    finally: server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', default=str(ROOT / '.private/evidence-hub'))
    commands = parser.add_subparsers(dest='command', required=True)
    serving = commands.add_parser('serve')
    serving.add_argument('--port', type=int, default=8765)
    serving.add_argument('--origin', help='Exact HTTPS Tailscale Serve origin')
    serving.add_argument('--owner', help='Exact Tailscale login permitted through Serve')
    serving.add_argument('--access', help='Private JSON containing exact origin and owner')
    commands.add_parser('status')
    importing = commands.add_parser('import', help='Register a reviewed private evidence record')
    importing.add_argument('record')
    candidate = commands.add_parser('candidate'); candidate.add_argument('record')
    checkpoint = commands.add_parser('checkpoint', help='Prepare strict private checkpoint helper data')
    checkpoint.add_argument('--point', required=True); checkpoint.add_argument('--output', required=True)
    opening = commands.add_parser('open', help='Normal pinned game launch; never restart or install')
    opening.add_argument('--inspection', required=True); opening.add_argument('--window-mode', required=True)
    opening.add_argument('--output', required=True); opening.add_argument('--focus', action='store_true')
    opening.add_argument('--restart', action='store_true', help='Normal close only; never force termination')
    opening.add_argument('--allow-hung-termination', action='store_true', help='Explicit owner-approved recovery of the exact unresponsive process; may lose unsaved progress')
    work = commands.add_parser('work'); work.add_argument('--once', action='store_true')
    work.add_argument('--config', help='Reviewed private runtime configuration')
    work.add_argument('--authored-results', help='Authored runner fixture JSON; never runtime evidence')
    args = parser.parse_args()
    try:
        store = Store(args.state)
        if args.command == 'serve':
            if args.access:
                access = json.loads(Path(args.access).read_text())
                args.origin, args.owner = access['origin'], access['owner']
            if bool(args.origin) != bool(args.owner): raise ValueError('Remote review requires both origin and owner')
            if args.origin and (not args.origin.startswith('https://') or urlsplit(args.origin).path):
                raise ValueError('Use an exact HTTPS origin without a trailing slash')
            serve(store, args.port, args.origin, args.owner)
        elif args.command == 'status': print(json.dumps(store.snapshot()))
        elif args.command == 'import': print(json.dumps(store.add_attempt(json.loads(Path(args.record).read_text()))))
        elif args.command == 'candidate': store.set_candidate(json.loads(Path(args.record).read_text()))
        elif args.command == 'checkpoint':
            from checkpoint import prepare
            print(json.dumps(prepare(args.point, args.output)))
        elif args.command == 'open':
            import os
            import subprocess
            def windows(path):
                if os.name == 'nt': return str(Path(path).resolve())
                return subprocess.check_output(['wslpath', '-w', str(Path(path).resolve())], text=True).strip()
            command = ['powershell' if os.name == 'nt' else 'powershell.exe', '-NoProfile', '-NonInteractive',
                       '-ExecutionPolicy', 'Bypass', '-File', windows(ROOT / 'tools/workbench/open.ps1'),
                       '-Inspection', windows(args.inspection), '-WindowMode', windows(args.window_mode),
                       '-Output', windows(args.output)]
            if args.focus: command.append('-Focus')
            if args.restart: command.append('-Restart')
            if args.allow_hung_termination: command.append('-AllowHungTermination')
            return subprocess.call(command)
        elif args.command == 'work':
            from gta_trial import work
            fixtures = json.loads(Path(args.authored_results).read_text()) if args.authored_results else None
            work(store, args.config, args.once, fixtures)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('Evidence hub unavailable; inspect private configuration.', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
