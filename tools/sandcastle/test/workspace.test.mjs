import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, mkdir, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { checked } from '../scripts/process.mjs';
import { requireWorkspace, preserveWorkspace } from '../scripts/workspace.mjs';

test('workspace rejects branch or revision drift and preserves uncommitted source', async t => {
  const root = await mkdtemp(join(tmpdir(), 'combine-workspace-'));
  try {
    const git = args => checked('git', ['-C', root, ...args]);
    await git(['init', '-q', '-b', 'main']);
    await git(['config', 'user.name', 'Test']);
    await git(['config', 'user.email', 'test@example.invalid']);
    await writeFile(join(root, 'source.txt'), 'baseline');
    await git(['add', 'source.txt']);
    await git(['commit', '-qm', 'baseline']);
    const base = await git(['rev-parse', 'HEAD']);
    await requireWorkspace(root, 'main', base);
    await assert.rejects(requireWorkspace(root, 'fix/other', base));
    await assert.rejects(requireWorkspace(root, 'main', '0'.repeat(40)));
    await writeFile(join(root, 'source.txt'), 'changed');
    await writeFile(join(root, 'new.txt'), 'new source');
    const evidence = await mkdtemp(join(tmpdir(), 'combine-evidence-'));
    t.after(() => rm(evidence, { recursive: true, force: true }));
    await preserveWorkspace(root, base, evidence);
    assert.match(await readFile(join(evidence, 'source.patch'), 'utf8'), /changed/);
    assert.equal(await readFile(join(root, 'new.txt'), 'utf8'), 'new source');
    assert.match(await readFile(join(evidence, 'status.txt'), 'utf8'), /new.txt/);
    assert.equal(await git(['rev-parse', 'HEAD']), base);
    await assert.rejects(requireWorkspace(root, 'main', base));
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
