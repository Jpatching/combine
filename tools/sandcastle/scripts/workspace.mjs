import { mkdir, writeFile, readFile, chmod } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { checked } from './process.mjs';
import { PRIVATE, REMOTE } from './settings.mjs';

// Generated Git config must not execute hooks, fsmonitor, pagers or diff helpers on the host.
export const gitAt = (repo, args, options) => checked('git', [
  '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
  '-c', 'core.untrackedCache=false', '-c', 'core.pager=cat', '-C', repo, ...args,
], options);

export async function requireWorkspace(repo, branch, revision) {
  if (await gitAt(repo, ['branch', '--show-current']) !== branch ||
      await gitAt(repo, ['rev-parse', 'HEAD']) !== revision ||
      await gitAt(repo, ['status', '--porcelain'])) {
    throw new Error('Checkout branch, revision or clean-tree invariant failed. Preserve the workspace before continuing.');
  }
}

export async function preserveWorkspace(repo, base, evidence) {
  // Leave untracked/ignored source in its worktree, never reset or checkpoint it with host-side git add.
  await writeFile(join(evidence, 'source.patch'), await gitAt(repo,
    ['diff', '--no-ext-diff', '--no-textconv', '--binary', base]), { mode: 0o600 });
  await writeFile(join(evidence, 'status.txt'), await gitAt(repo,
    ['status', '--porcelain', '--untracked-files=all']), { mode: 0o600 });
}

export async function authHome(id) {
  await mkdir(PRIVATE, { recursive: true, mode: 0o700 });
  await chmod(PRIVATE, 0o700);
  const home = join(PRIVATE, 'auth', id);
  await mkdir(home, { recursive: true, mode: 0o700 });
  const source = join(process.env.CODEX_HOME ?? join(homedir(), '.codex'), 'auth.json');
  const auth = JSON.parse(await readFile(source, 'utf8'));
  if (auth.auth_mode !== 'chatgpt' || !auth.tokens || auth.OPENAI_API_KEY) {
    throw new Error('ChatGPT file authentication is required; API fallback is disabled.');
  }
  await writeFile(join(home, 'auth.json'), JSON.stringify({ auth_mode: auth.auth_mode, tokens: auth.tokens }), { mode: 0o600 });
  return home;
}

export async function sourceClone(id, base, signal) {
  const repo = join(PRIVATE, 'repos', id);
  const home = join(PRIVATE, 'host-home', id);
  await mkdir(home, { recursive: true, mode: 0o700 });
  const env = { PATH: process.env.PATH, HOME: home, LANG: 'C.UTF-8', GIT_CONFIG_NOSYSTEM: '1', GIT_TERMINAL_PROMPT: '0' };
  await checked('git', ['-c', 'credential.helper=', '-c', 'core.hooksPath=/dev/null',
    'clone', '--single-branch', '--branch', 'main', REMOTE, repo], { env, signal, timeoutMs: 120_000 });
  await requireWorkspace(repo, 'main', base);
  const tracked = await gitAt(repo, ['ls-files', '-z']);
  if (tracked.split('\0').some(path => path === '.sandcastle/.env' ||
      path.startsWith('.private/') || path === '.env' || path.startsWith('.env.'))) {
    throw new Error('Source snapshot includes private environment configuration.');
  }
  await gitAt(repo, ['remote', 'remove', 'origin']);
  await gitAt(repo, ['config', 'user.name', 'Combine Sandcastle']);
  await gitAt(repo, ['config', 'user.email', 'sandcastle@example.invalid']);
  return repo;
}
