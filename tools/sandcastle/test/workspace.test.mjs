import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm, chmod, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { checked, execute } from '../scripts/process.mjs';
import { requireWorkspace, preserveWorkspace, hostGitEnv } from '../scripts/workspace.mjs';

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

test('dependency-owned host Git cannot lazy-fetch through a configured remote helper', async t => {
  const root = await mkdtemp(join(tmpdir(), 'combine-lazy-fetch-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const git = (args, options) => checked('git', ['-C', root, ...args], options);
  await git(['init', '-q', '-b', 'main']);
  const tree = await git(['hash-object', '-t', 'tree', '-w', '--stdin'], { input: '' });
  const missingParent = '1'.repeat(40);
  const commit = await git(['hash-object', '-t', 'commit', '-w', '--stdin'], {
    input: `tree ${tree}\nparent ${missingParent}\nauthor Test <test@example.invalid> 1 +0000\ncommitter Test <test@example.invalid> 1 +0000\n\nMissing parent fixture\n`,
  });
  await git(['update-ref', 'refs/heads/main', commit]);
  const marker = join(root, 'HOST_REMOTE_HELPER_EXECUTED');
  const helper = join(root, 'remote-helper.sh');
  await writeFile(helper, `#!/bin/sh\ntouch '${marker}'\nexit 1\n`);
  await chmod(helper, 0o700);
  for (const [key, value] of [['core.repositoryformatversion', '1'], ['extensions.partialClone', 'trap'],
    ['remote.trap.promisor', 'true'], ['remote.trap.url', `ext::${helper}`], ['protocol.ext.allow', 'always']]) {
    await git(['config', key, value]);
  }
  const result = await execute('git', ['-C', root, 'rev-list', 'main', '--reverse'],
    { env: { ...process.env, ...hostGitEnv() }, timeoutMs: 5000 });
  assert.notEqual(result.code, 0);
  assert.equal(result.reason, null);
  await assert.rejects(access(marker));
});
