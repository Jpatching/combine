import { createSandbox } from '@ai-hero/sandcastle';
import { docker } from '@ai-hero/sandcastle/sandboxes/docker';

// Keep Docker teardown separate from the SDK's source-removing worktree cleanup.
export async function retainedSandbox({ cwd, branch, baseBranch, image, auth }) {
  const provider = docker({ imageName: image, selinuxLabel: false, cpus: 2,
    env: auth ? { CODEX_HOME: '/home/agent/.codex' } : {},
    mounts: auth ? [{ hostPath: auth, sandboxPath: '/home/agent/.codex' }] : [] });
  let handle;
  const sandbox = await createSandbox({ cwd, branch, baseBranch,
    sandbox: { ...provider, async create(options) {
      handle = await provider.create(options);
      return handle;
    } },
    hooks: { sandbox: { onSandboxReady: [{ command: 'git config --global user.name "Combine Sandcastle" && git config --global user.email sandcastle@example.invalid' }] } },
  });
  return { worktreePath: sandbox.worktreePath, run: options => sandbox.run(options),
    stop: async () => { if (handle) { await handle.close(); handle = undefined; } } };
}
