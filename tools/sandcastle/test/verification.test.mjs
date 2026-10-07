import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, lstat, readdir, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { verifierArgs, prepareScratch } from '../scripts/verification.mjs';

test('verifier has no credentials or network and only read-only source mounts', () => {
  const args = verifierArgs('check', '/trial/worktree', '/trial/repo');
  assert.equal(args[args.indexOf('--network') + 1], 'none');
  assert.ok(args.includes('--read-only'));
  const mounts = args.filter((value, index) => args[index - 1] === '-v');
  assert.equal(mounts.length, 3);
  assert.ok(mounts.every(value => value.endsWith(':ro')));
  assert.ok(mounts.every(value => !/\/auth\/|docker.sock|\.codex/.test(value)));
  assert.ok(args.includes(`/trial/worktree/.private:rw,nosuid,nodev,noexec,uid=${process.getuid()},gid=${process.getgid()},mode=0700`));
});

test('scratch creates a private empty mountpoint and accepts an existing real directory', async t => {
  const root = await mkdtemp(join(tmpdir(), 'combine-scratch-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  await prepareScratch(root);
  assert.equal((await lstat(join(root, '.private'))).mode & 0o777, 0o700);
  assert.deepEqual(await readdir(join(root, '.private')), []);
  await prepareScratch(root);
});

test('scratch rejects symlinks and files without touching the target', async t => {
  const root = await mkdtemp(join(tmpdir(), 'combine-scratch-'));
  const target = await mkdtemp(join(tmpdir(), 'combine-scratch-target-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  t.after(() => rm(target, { recursive: true, force: true }));
  const scratch = join(root, '.private');
  await symlink(target, scratch);
  await assert.rejects(prepareScratch(root), /real directory/);
  assert.deepEqual(await readdir(target), []);
  assert.ok((await lstat(scratch)).isSymbolicLink());
  await rm(scratch);
  await writeFile(scratch, 'not a directory');
  await assert.rejects(prepareScratch(root), /real directory/);
});
