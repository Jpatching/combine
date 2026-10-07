import test from 'node:test';
import assert from 'node:assert/strict';
import { verifierArgs } from '../scripts/verification.mjs';

test('verifier has no credentials or network and only read-only source mounts', () => {
  const args = verifierArgs('check', '/trial/worktree', '/trial/repo');
  assert.equal(args[args.indexOf('--network') + 1], 'none');
  assert.ok(args.includes('--read-only'));
  const mounts = args.filter((value, index) => args[index - 1] === '-v');
  assert.equal(mounts.length, 3);
  assert.ok(mounts.every(value => value.endsWith(':ro')));
  assert.ok(mounts.every(value => !/\/auth\/|docker.sock|\.codex/.test(value)));
});
