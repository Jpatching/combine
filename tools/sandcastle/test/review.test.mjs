import test from 'node:test';
import assert from 'node:assert/strict';
import { reviewArgs } from '../scripts/review.mjs';

test('review commands use the external Docker boundary with read-only source and Git', () => {
  const args = reviewArgs('review', '/trial/worktree', '/trial/repo', '/trial/auth');
  assert.ok(args.includes('--read-only'));
  assert.ok(args.includes('--cap-drop=ALL'));
  assert.ok(args.includes('--security-opt=no-new-privileges'));
  assert.equal(args[args.indexOf('-s') + 1], 'danger-full-access');
  const mounts = args.filter((value, index) => args[index - 1] === '-v');
  assert.deepEqual(mounts, ['/trial/worktree:/trial/worktree:ro', '/trial/repo/.git:/trial/repo/.git:ro', '/trial/auth:/auth']);
  assert.ok(args.includes('--ephemeral'));
  assert.ok(args.includes('--ignore-user-config'));
  assert.ok(args.includes('--ignore-rules'));
});
