import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile, access } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { createSandbox } from '@ai-hero/sandcastle';
import { docker } from '@ai-hero/sandcastle/sandboxes/docker';
import { gitAt, preserveWorkspace } from '../scripts/workspace.mjs';
import { verify } from '../scripts/verification.mjs';
import { PRIVATE, ROOT, IMAGE } from '../scripts/settings.mjs';

async function fixture() {
  const dir = join(PRIVATE, 'integration', randomUUID());
  const repo = join(dir, 'repo');
  await mkdir(join(repo, 'scripts'), { recursive: true, mode: 0o700 });
  await gitAt(repo, ['init', '-q', '-b', 'main']);
  await gitAt(repo, ['config', 'user.name', 'Integration Test']);
  await gitAt(repo, ['config', 'user.email', 'test@example.invalid']);
  await writeFile(join(repo, 'scripts/verify.py'), 'assert False, "seeded failure"\n');
  await gitAt(repo, ['add', '.']);
  await gitAt(repo, ['commit', '-qm', 'Source-only test baseline']);
  return { dir, repo, base: await gitAt(repo, ['rev-parse', 'HEAD']) };
}

test('Docker verifier rejects a defect, accepts a fix and enforces isolation', async () => {
  const { dir, repo } = await fixture();
  const task = { checks: [] };
  assert.equal((await verify(repo, repo, task)).passed, false);
  const marker = join(dir, 'outside-private-marker');
  await writeFile(marker, 'not mounted');
  await writeFile(join(repo, 'scripts/verify.py'), [
    'import os, socket', 'from pathlib import Path',
    'assert "CODEX_HOME" not in os.environ', 'assert "OPENAI_API_KEY" not in os.environ',
    'assert not Path("/auth/auth.json").exists()', 'assert not Path("/home/agent/.codex/auth.json").exists()',
    `assert not Path(${JSON.stringify(marker)}).exists()`,
    `assert not Path(${JSON.stringify(join(ROOT, '.private/worktrees'))}).exists()`,
    'try:', '    Path("scripts/verify.py").write_text("bad")',
    'except OSError:', '    pass', 'else:', '    raise AssertionError("source is writable")',
    'with socket.socket() as s:', '    s.settimeout(1)',
    '    try:', '        s.connect(("1.1.1.1", 443))', '    except OSError:', '        pass',
    '    else:', '        raise AssertionError("network available")', 'print("PASS: verifier isolation")',
  ].join('\n'));
  const outcome = await verify(repo, repo, task);
  assert.equal(outcome.passed, true, JSON.stringify(outcome));
  assert.match(await readFile(join(repo, 'scripts/verify.py'), 'utf8'), /verifier isolation/);
});

test('Sandcastle cancellation retains dirty source, task branch and baseline', async () => {
  const { dir, repo, base } = await fixture();
  const branch = `test/cancel-${randomUUID()}`;
  const controller = new AbortController();
  const sandbox = await createSandbox({ cwd: repo, branch, baseBranch: base,
    sandbox: docker({ imageName: IMAGE, selinuxLabel: false }) });
  const localAgent = {
    name: 'deterministic-test', env: {}, captureSessions: false,
    buildPrintCommand: () => ({ command: 'touch CHECKPOINT.txt; printf "READY\\n"; sleep 60' }),
    buildInteractiveArgs: () => [],
    parseStreamLine: line => line.trim() === 'READY' ? [{ type: 'text', text: 'READY' }] : [],
  };
  const timer = setTimeout(() => controller.abort(), 10_000);
  let closed;
  try {
    await assert.rejects(sandbox.run({ agent: localAgent, prompt: 'deterministic cancellation test',
      signal: controller.signal, maxIterations: 1,
      logging: { type: 'file', path: join(dir, 'cancel.log'), onAgentStreamEvent(event) {
        if (event.type === 'text' && event.message.includes('READY')) controller.abort();
      } },
    }));
    await access(join(sandbox.worktreePath, 'CHECKPOINT.txt'));
    await preserveWorkspace(sandbox.worktreePath, base, dir);
    assert.match(await readFile(join(dir, 'status.txt'), 'utf8'), /CHECKPOINT.txt/);
    assert.equal(await gitAt(repo, ['rev-parse', 'main']), base);
    assert.equal(await gitAt(sandbox.worktreePath, ['branch', '--show-current']), branch);
  } finally {
    clearTimeout(timer);
    closed = await sandbox.close();
  }
  assert.equal(closed.preservedWorktreePath, sandbox.worktreePath);
  await access(join(sandbox.worktreePath, 'CHECKPOINT.txt'));
});
