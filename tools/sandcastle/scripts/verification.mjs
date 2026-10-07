import { randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { mkdir } from 'node:fs/promises';
import { execute } from './process.mjs';
import { hostGitEnv } from './workspace.mjs';
import { IMAGE, TOOL } from './settings.mjs';

export function verifierArgs(name, worktree, repo, image = IMAGE) {
  return ['run', '--rm', '--name', name, '--network', 'none', '--read-only',
    '--cap-drop=ALL', '--security-opt=no-new-privileges', '--pids-limit=256',
    '--memory=512m', '--cpus=2', '--tmpfs', '/tmp',
    '--user', `${process.getuid()}:${process.getgid()}`,
    '-v', `${worktree}:${worktree}:ro`, '-v', `${join(repo, '.git')}:${join(repo, '.git')}:ro`,
    '-v', `${join(TOOL, 'acceptance')}:/checks:ro`,
    '-e', 'HOME=/tmp', '-e', 'PYTHONDONTWRITEBYTECODE=1',
    '-e', 'GIT_CONFIG_COUNT=2', '-e', 'GIT_CONFIG_KEY_0=core.fsmonitor', '-e', 'GIT_CONFIG_VALUE_0=false',
    '-e', 'GIT_CONFIG_KEY_1=core.hooksPath', '-e', 'GIT_CONFIG_VALUE_1=/dev/null',
    '-w', worktree, '--entrypoint', 'python3', image];
}

export async function verify(worktree, repo, task, options = {}) {
  const { image = IMAGE, ...executionOptions } = options;
  const revision = await inspectGit(worktree, repo, ['rev-parse', 'HEAD'], { ...executionOptions, image });
  const executions = [];
  for (const [command, ...args] of [['python3', 'scripts/verify.py'], ...task.checks]) {
    if (command !== 'python3') throw new Error('Unsupported check tool; add a reviewed check profile.');
    const name = `combine-check-${randomUUID()}`;
    let result;
    try {
      result = await execute('docker', [...verifierArgs(name, worktree, repo, image), ...args], executionOptions);
    } finally {
      await execute('docker', ['rm', '-f', name], { timeoutMs: 20_000 });
    }
    executions.push({ command: [command, ...args], ...result });
    if (result.code !== 0 || result.reason) break;
  }
  return { revision, passed: executions.length === task.checks.length + 1 &&
    executions.every(result => result.code === 0 && !result.reason), executions };
}

export async function inspectGit(worktree, repo, args, { image = IMAGE, ...options } = {}) {
  const name = `combine-inspect-${randomUUID()}`;
  const command = verifierArgs(name, worktree, repo, image);
  command[command.indexOf('--entrypoint') + 1] = 'git';
  // Environment protects common helpers; any remaining configured filters stay
  // inside this read-only, credential-free, network-disabled container.
  command.splice(command.indexOf('-w'), 0, ...Object.entries(hostGitEnv()).flatMap(([key, value]) => ['-e', `${key}=${value}`]));
  let result;
  try { result = await execute('docker', [...command, ...args], options); }
  finally { await execute('docker', ['rm', '-f', name], { timeoutMs: 20_000 }); }
  if (result.code !== 0 || result.reason) throw new Error('Isolated Git inspection failed.');
  return result.stdout.trim();
}

export async function requireIsolatedWorkspace(worktree, repo, branch, revision, options) {
  if (await inspectGit(worktree, repo, ['branch', '--show-current'], options) !== branch ||
      await inspectGit(worktree, repo, ['rev-parse', 'HEAD'], options) !== revision ||
      await inspectGit(worktree, repo, ['status', '--porcelain'], options)) {
    throw new Error('Isolated checkout branch, revision or clean-tree invariant failed.');
  }
}

export async function exportBranchBundle(worktree, repo, evidence, branch, base, image) {
  const name = `combine-export-${randomUUID()}`;
  const output = join(evidence, 'export');
  await mkdir(output, { mode: 0o700 });
  const args = verifierArgs(name, worktree, repo, image);
  args[args.indexOf('--entrypoint') + 1] = 'git';
  args.splice(args.indexOf('-w'), 0, '-v', `${output}:/export`);
  let result;
  try {
    result = await execute('docker', [...args, 'bundle', 'create', '/export/task.bundle',
      branch, `^${base}`], { timeoutMs: 30_000 });
  } finally { await execute('docker', ['rm', '-f', name], { timeoutMs: 20_000 }); }
  if (result.code !== 0 || result.reason) throw new Error('Isolated task bundle export failed.');
  return join(output, 'task.bundle');
}
