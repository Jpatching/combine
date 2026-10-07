import { spawn } from 'node:child_process';

// A child process is the public boundary: capture output, bound runtime, kill
// the entire process group so a subprocess cannot survive cancellation.
export function execute(command, args, { cwd, env = process.env, timeoutMs = 30_000, signal, input, onLine, killGraceMs = 1000, cancellationMessage } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, env, detached: true, stdio: ['pipe', 'pipe', 'pipe'] });
    let stdout = '', stderr = '', reason = null;
    let pending = '';
    let force;
    let stopping = false;
    function kill() {
      if (stopping) return;
      stopping = true;
      if (cancellationMessage) child.stdin.write(cancellationMessage);
      else { try { process.kill(-child.pid, 'SIGTERM'); } catch {} }
      force = setTimeout(() => { try { process.kill(-child.pid, 'SIGKILL'); } catch {} }, killGraceMs);
      force.unref();
    }
    const abort = () => { reason = 'cancelled'; kill(); };
    const timer = setTimeout(() => { reason = 'timeout'; kill(); }, timeoutMs);
    child.on('error', error => { clearTimeout(timer); clearTimeout(force); signal?.removeEventListener('abort', abort); reject(error); });
    child.stdout.on('data', chunk => {
      const text = chunk.toString();
      stdout = (stdout + text).slice(-2_000_000);
      pending += text;
      const lines = pending.split('\n');
      pending = lines.pop();
      for (const line of lines) onLine?.(line);
    });
    child.stderr.on('data', chunk => { stderr = (stderr + chunk.toString()).slice(-2_000_000); });
    child.on('close', code => {
      clearTimeout(timer); clearTimeout(force); signal?.removeEventListener('abort', abort);
      if (pending) onLine?.(pending);
      resolve({ code, stdout, stderr, reason });
    });
    signal?.addEventListener('abort', abort, { once: true });
    if (signal?.aborted) abort();
    child.stdin.on('error', () => {});
    if (cancellationMessage) { if (input) child.stdin.write(input); }
    else child.stdin.end(input ?? '');
  });
}

export async function checked(command, args, options) {
  const result = await execute(command, args, options);
  if (result.code !== 0 || result.reason) throw new Error(`${command} ${args[0] ?? ''} failed (${result.reason ?? result.code}): ${result.stderr.slice(-2000)}`);
  return result.stdout.trim();
}
