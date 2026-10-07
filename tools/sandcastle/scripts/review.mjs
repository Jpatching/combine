import { randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { execute } from './process.mjs';
import { IMAGE, MODEL, EFFORT } from './settings.mjs';
import { parseReview } from './policy.mjs';

export function agentMessage(stdout) {
  let text = '', complete = false;
  for (const line of stdout.split('\n')) {
    try {
      const event = JSON.parse(line);
      if (['error', 'turn.failed'].includes(event.type)) throw new Error('Agent inference failed.');
      if (event.type === 'turn.completed') complete = true;
      if (event.type === 'item.completed' && event.item?.type === 'agent_message') text += event.item.text + '\n';
    } catch (error) {
      if (!(error instanceof SyntaxError)) throw error;
    }
  }
  if (!complete) throw new Error('Agent turn did not complete.');
  return text;
}

export async function freshReview(axis, worktree, repo, home, prompt, revision, options) {
  const { image = IMAGE, ...executionOptions } = options;
  const name = `combine-review-${axis}-${randomUUID()}`;
  let execution;
  try {
    execution = await execute('docker', [
      'run', '--rm', '-i', '--name', name, '--read-only', '--tmpfs', '/tmp',
      '--cap-drop=ALL', '--security-opt=no-new-privileges', '--pids-limit=256', '--cpus=2',
      '--user', `${process.getuid()}:${process.getgid()}`,
      '-v', `${worktree}:${worktree}:ro`, '-v', `${join(repo, '.git')}:${join(repo, '.git')}:ro`,
      '-v', `${home}:/auth`, '-e', 'CODEX_HOME=/auth', '-e', 'HOME=/tmp',
      '-e', 'PYTHONDONTWRITEBYTECODE=1', '-w', worktree, '--entrypoint', 'codex', image,
      'exec', '--json', '--ephemeral', '--ignore-user-config', '--ignore-rules',
      '--skip-git-repo-check', '-s', 'read-only', '-c', 'approval_policy="never"',
      '-m', MODEL, '-c', `model_reasoning_effort="${EFFORT}"`, '-',
    ], { ...executionOptions, input: prompt });
    if (execution.code !== 0 || execution.reason) throw new Error(`Fresh ${axis} review failed.`);
    return { execution, review: parseReview(agentMessage(execution.stdout), revision) };
  } finally {
    await execute('docker', ['rm', '-f', name], { timeoutMs: 20_000 });
  }
}
