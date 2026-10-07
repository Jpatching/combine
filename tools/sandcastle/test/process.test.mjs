import assert from 'node:assert/strict';
import test from 'node:test';
import { execute } from '../scripts/process.mjs';

test('child failures are returned, not reported as success', async () => {
  const result = await execute(process.execPath, ['-e', 'console.error("failed check"); process.exit(7)']);
  assert.equal(result.code, 7);
  assert.match(result.stderr, /failed check/);
});

test('timeout stops a hanging child and preserves its output', async () => {
  const result = await execute(process.execPath, ['-e', 'console.log("checkpoint"); setInterval(() => {}, 1000)'], { timeoutMs: 300 });
  assert.equal(result.reason, 'timeout');
  assert.match(result.stdout, /checkpoint/);
});

test('cancellation stops a running child', async () => {
  const controller = new AbortController();
  const resultPromise = execute(process.execPath, ['-e', 'setInterval(() => {}, 1000)'], { signal: controller.signal });
  setTimeout(() => controller.abort(), 100);
  assert.equal((await resultPromise).reason, 'cancelled');
});

test('stdin and streamed lines reach the child and caller', async () => {
  const lines = [];
  const result = await execute(process.execPath, ['-e', 'process.stdin.pipe(process.stdout)'], { input: 'brief\n', onLine: line => lines.push(line) });
  assert.equal(result.code, 0);
  assert.deepEqual(lines, ['brief']);
});

test('cooperative cancellation allows a worker to preserve its checkpoint before exit', async () => {
  const controller = new AbortController();
  const resultPromise = execute(process.execPath, ['-e', 'process.stdin.on("data", () => setTimeout(() => { console.log("checkpoint preserved"); process.exit(0); }, 100)); console.log("ready")'], {
    signal: controller.signal, cancellationMessage: 'CANCEL\n', killGraceMs: 2000,
    onLine: line => { if (line === 'ready') controller.abort(); },
  });
  const result = await resultPromise;
  assert.equal(result.reason, 'cancelled');
  assert.equal(result.code, 0);
  assert.match(result.stdout, /checkpoint preserved/);
});
