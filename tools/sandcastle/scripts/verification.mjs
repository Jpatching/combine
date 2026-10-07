import { randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { execute } from './process.mjs';
import { gitAt } from './workspace.mjs';
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
  const revision = await gitAt(worktree, ['rev-parse', 'HEAD']);
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
