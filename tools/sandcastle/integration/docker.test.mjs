import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile, access, chmod, readdir } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { gitAt, preserveWorkspace, hostGitEnv, sourceClone } from '../scripts/workspace.mjs';
import { verify, inspectGit, exportBranchBundle } from '../scripts/verification.mjs';
import { retainedSandbox } from '../scripts/sandbox.mjs';
import { reviewArgs } from '../scripts/review.mjs';
import { checked } from '../scripts/process.mjs';
import { PRIVATE, ROOT, IMAGE } from '../scripts/settings.mjs';

Object.assign(process.env, hostGitEnv());

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

test('actual Combine gate can use empty ephemeral private scratch without host persistence', async () => {
  const base = await gitAt(ROOT, ['rev-parse', 'main']);
  const repo = await sourceClone(`gate-${randomUUID()}`, base);
  const result = await verify(repo, repo, { checks: [] });
  assert.equal(result.passed, true, JSON.stringify(result));
  assert.deepEqual(await readdir(join(repo, '.private')), []);
});

test('reviewer shell reads source but cannot write source, Git metadata or container root', async () => {
  const { dir, repo, base } = await fixture();
  const home = join(dir, 'dummy-auth');
  await mkdir(home);
  const args = reviewArgs(`combine-review-test-${randomUUID()}`, repo, repo, home, IMAGE);
  args.splice(args.indexOf(IMAGE) + 1);
  args[args.indexOf('--entrypoint') + 1] = 'python3';
  const output = await checked('docker', [...args, '-c', [
    'from pathlib import Path',
    'assert "seeded failure" in Path("scripts/verify.py").read_text()',
    'for path in ("scripts/verify.py", ".git/config", "/reviewer-write-probe"):',
    '    try:', '        Path(path).write_text("bad")',
    '    except OSError:', '        pass',
    '    else:', '        raise AssertionError("reviewer can write " + path)',
    'Path("/tmp/review-probe").write_text("temporary")',
    'Path("/auth/review-probe").write_text("dedicated auth")',
    'assert not Path("/var/run/docker.sock").exists()',
    `assert not Path(${JSON.stringify(join(ROOT, '.private/worktrees'))}).exists()`,
    'print("PASS: Docker review boundary")',
  ].join('\n')], { timeoutMs: 20_000 });
  assert.match(output, /PASS: Docker review boundary/);
  assert.equal(await gitAt(repo, ['rev-parse', 'HEAD']), base);
  assert.equal(await gitAt(repo, ['status', '--porcelain']), '');
});

test('accepted task commits export as a source bundle from the isolated inspector', async () => {
  const { dir, repo, base } = await fixture();
  const branch = `test/bundle-${randomUUID()}`;
  await gitAt(repo, ['checkout', '-qb', branch]);
  await writeFile(join(repo, 'scripts/verify.py'), 'assert True\n');
  await gitAt(repo, ['add', 'scripts/verify.py']);
  await gitAt(repo, ['commit', '-qm', 'Accepted synthetic task']);
  const revision = await gitAt(repo, ['rev-parse', 'HEAD']);
  const bundle = await exportBranchBundle(repo, repo, dir, branch, base, IMAGE);
  await gitAt(repo, ['bundle', 'verify', bundle]);
  assert.match(await gitAt(repo, ['bundle', 'list-heads', bundle]), new RegExp(revision));
});

test('Git helpers stay isolated and stopping Docker retains ignored source even if copying fails', async () => {
  const { dir, repo, base } = await fixture();
  const branch = `test/ignored-${randomUUID()}`;
  const sandbox = await retainedSandbox({ cwd: repo, branch, baseBranch: base, image: IMAGE });
  const worktree = sandbox.worktreePath;
  try {
    await writeFile(join(repo, '.git/info/exclude'), 'ignored-recovery/\n');
    await mkdir(join(worktree, 'ignored-recovery'));
    await writeFile(join(worktree, 'ignored-recovery/source.txt'), 'retained after cleanup');
    const marker = join(dir, 'HOST_HELPER_EXECUTED');
    const helper = join(dir, 'fsmonitor.sh');
    await writeFile(helper, `#!/bin/sh\ntouch '${marker}'\n`);
    await chmod(helper, 0o700);
    await gitAt(repo, ['config', 'core.fsmonitor', helper]);
    const filter = join(worktree, 'filter.sh');
    await writeFile(filter, `#!/bin/sh\ntouch '${marker}'\ncat\n`);
    await chmod(filter, 0o700);
    await writeFile(join(repo, '.git/info/attributes'), 'scripts/verify.py filter=hostprobe\n');
    await gitAt(repo, ['config', 'filter.hostprobe.clean', filter]);
    await writeFile(join(worktree, 'scripts/verify.py'), 'assert True, "changed source length"\n');
    await sandbox.stop();
    const inspect = args => inspectGit(worktree, repo, args);
    assert.match(await inspect(['status', '--porcelain']), /scripts\/verify.py/);
    await writeFile(join(dir, 'copy-blocked'), 'not a directory');
    await assert.rejects(preserveWorkspace(worktree, base, join(dir, 'copy-blocked'), inspect));
    assert.equal(await readFile(join(worktree, 'ignored-recovery/source.txt'), 'utf8'), 'retained after cleanup');
    await preserveWorkspace(worktree, base, dir, inspect);
    await assert.rejects(access(marker));
    assert.equal(await readFile(join(dir, 'source/ignored-recovery/source.txt'), 'utf8'), 'retained after cleanup');
    assert.equal(await gitAt(repo, ['rev-parse', branch]), base);
  } finally { await sandbox.stop(); }
});

test('Sandcastle cancellation retains dirty source, task branch and baseline', async () => {
  const { dir, repo, base } = await fixture();
  const branch = `test/cancel-${randomUUID()}`;
  const controller = new AbortController();
  const sandbox = await retainedSandbox({ cwd: repo, branch, baseBranch: base, image: IMAGE });
  const localAgent = {
    name: 'deterministic-test', env: {}, captureSessions: false,
    buildPrintCommand: () => ({ command: 'touch CHECKPOINT.txt; printf "READY\\n"; sleep 60' }),
    buildInteractiveArgs: () => [],
    parseStreamLine: line => line.trim() === 'READY' ? [{ type: 'text', text: 'READY' }] : [],
  };
  const timer = setTimeout(() => controller.abort(), 10_000);
  try {
    await assert.rejects(sandbox.run({ agent: localAgent, prompt: 'deterministic cancellation test',
      signal: controller.signal, maxIterations: 1,
      logging: { type: 'file', path: join(dir, 'cancel.log'), onAgentStreamEvent(event) {
        if (event.type === 'text' && event.message.includes('READY')) controller.abort();
      } },
    }));
    await access(join(sandbox.worktreePath, 'CHECKPOINT.txt'));
    await sandbox.stop();
    await preserveWorkspace(sandbox.worktreePath, base, dir,
      args => inspectGit(sandbox.worktreePath, repo, args));
    assert.match(await readFile(join(dir, 'status.txt'), 'utf8'), /CHECKPOINT.txt/);
    assert.equal(await gitAt(repo, ['rev-parse', 'main']), base);
    assert.equal(await gitAt(sandbox.worktreePath, ['branch', '--show-current']), branch);
  } finally {
    clearTimeout(timer);
    await sandbox.stop();
  }
  await access(join(sandbox.worktreePath, 'CHECKPOINT.txt'));
});

test('public-source report verifier rejects unsupported evidence and preserves the report', async () => {
  const { dir, repo, base } = await fixture();
  const path = 'research/results/report.md';
  await mkdir(join(repo, 'research/results'), { recursive: true });
  await writeFile(join(repo, 'scripts/verify.py'), 'assert True\n');
  const revision = 'a'.repeat(40);
  const url = `https://github.com/owner/source/blob/${revision}/collision.cpp`;
  const text = `# Public-source report\n\n## Verified source facts\n[Source](${url}).\n\n## Source inference\nPort unproven.\n\n## Unknowns\nRuntime behavior.\n\n## Next local proof\nObserve a floor.\n\n<research>${JSON.stringify({ verdict: 'requires-local-proof', runtimeVerified: false, sources: [{ url, revision }], unknowns: ['Runtime behavior'], inaccessibleSources: [] })}</research>\n`;
  const task = { checks: [['python3', '/checks/research_report.py', path]] };
  await writeFile(join(repo, path), text);
  assert.equal((await verify(repo, repo, task)).passed, true);
  const invalid = text.replace('"runtimeVerified":false', '"runtimeVerified":true');
  await writeFile(join(repo, path), invalid);
  assert.equal((await verify(repo, repo, task)).passed, false);
  await preserveWorkspace(repo, base, dir, args => inspectGit(repo, repo, args));
  assert.equal(await readFile(join(dir, 'source', path), 'utf8'), invalid);
});
