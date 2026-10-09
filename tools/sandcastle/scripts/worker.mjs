import { writeFile, readFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { performance } from 'node:perf_hooks';
import { codex } from '@ai-hero/sandcastle';
import { PRIVATE, MODEL, EFFORT, LIMIT_MS, PINS } from './settings.mjs';
import { requireWorkspace, preserveWorkspace, hostGitEnv } from './workspace.mjs';
import { verify, inspectGit, requireIsolatedWorkspace, exportBranchBundle } from './verification.mjs';
import { retainedSandbox } from './sandbox.mjs';
import { freshReview } from './review.mjs';
import { researcherPrompt } from './research.mjs';
import { acceptResult } from './policy.mjs';

const [runDir] = process.argv.slice(2);
Object.assign(process.env, hostGitEnv());
const job = JSON.parse(await readFile(join(runDir, 'job.json'), 'utf8'));
const research = job.task.kind === 'research';
const started = performance.now();
const controller = new AbortController();
let cancelled = false, sandbox;
const cancel = () => { cancelled = true; controller.abort(); };
process.on('SIGINT', cancel);
process.on('SIGTERM', cancel);
// Cooperative cancellation avoids Sandcastle's process-exit handler racing preservation.
process.stdin.on('data', chunk => { if (chunk.toString().includes('CANCEL')) cancel(); });
const timer = setTimeout(() => controller.abort(), LIMIT_MS);
timer.unref();
const row = { kind: job.task.kind ?? 'coding', role: research ? 'background-researcher' : 'implementer', id: job.id, issue: job.issue.number, branch: job.branch, base: job.base,
  pins: PINS, image: job.image, model: MODEL, effort: EFFORT, status: 'running',
  startedAt: new Date().toISOString(), handsOnMinutes: null, interruptions: null, ownerAccepted: null,
  reviews: {}, repo: job.repo, worktree: null };
const save = () => writeFile(join(runDir, 'result.json'), JSON.stringify(row, null, 2), { mode: 0o600 });
const remaining = () => Math.max(1, LIMIT_MS - (performance.now() - started));
const options = () => ({ signal: controller.signal, timeoutMs: remaining() });
await save();

try {
  await requireWorkspace(job.repo, 'main', job.base);
  sandbox = await retainedSandbox({ cwd: job.repo, branch: job.branch, baseBranch: job.base,
    image: job.image, auth: job.auth });
  row.worktree = sandbox.worktreePath;
  // Persist recovery pointers before starting inference.
  await save();
  controller.signal.throwIfAborted();
  const brief = `Issue #${job.issue.number}: ${job.issue.title}\n${job.issue.body}\n\nComments:\n${job.issue.comments.map(comment => comment.body).join('\n\n')}`;
  const provider = codex(MODEL, { effort: EFFORT, captureSessions: false });
  const agent = { ...provider, buildPrintCommand(options) {
    const built = provider.buildPrintCommand(options);
    return { ...built, command: `${built.command} --ephemeral --ignore-user-config --ignore-rules` };
  } };
  let agentError = false;
  const output = await sandbox.run({ agent, maxIterations: 1, signal: controller.signal,
    completionSignal: '<promise>COMPLETE</promise>',
    logging: { type: 'file', path: join(runDir, 'implement.log'), verbose: true,
      onAgentStreamEvent(event) {
        if (event.type === 'raw') {
          try { if (['error', 'turn.failed'].includes(JSON.parse(event.line).type)) agentError = true; } catch {}
        }
      } },
    prompt: research ? researcherPrompt(job, brief) : [brief, job.skills.implement, job.skills.tdd,
      `You own only ${job.task.paths.join(', ')}. Other work is preserved; do not revert it.`,
      `This isolated chat workspace is /home/agent/workspace, branch ${job.branch}, starting revision ${job.base}. Verify it before editing and before committing.`,
      'The host already fetched and approved this single issue and its test seams. Host handles tracker, external verification, fresh Standards/Spec reviews and publication. Read AGENTS.md and referenced repository rules. Use the supplied original Matt skills; missing host skill paths are not installed in this container.',
      'Work one failing regression at a time at the existing check_links interface. Record the red test command/output in your final response. Then run focused tests and python3 scripts/verify.py, commit only scoped source changes on the current task branch, and explain verification.',
      'The external acceptance check is host-controlled. Stop if blocked; do not choose another task, invoke nested agents, publish, access game assets or change protection behavior.',
      'Emit <promise>COMPLETE</promise> only after checks pass and the task changes are committed.',
    ].join('\n\n'),
  });
  await sandbox.stop();
  await writeFile(join(runDir, 'implement.txt'), output.stdout, { mode: 0o600 });
  row.usage = output.iterations.map(iteration => iteration.usage ?? null);
  if (agentError || !output.completionSignal) throw new Error('Implementer did not complete successfully.');
  if (research) row.researcherCompleted = true;
  const inspection = { ...options(), image: job.image };
  row.revision = await inspectGit(row.worktree, job.repo, ['rev-parse', 'HEAD'], inspection);
  await requireIsolatedWorkspace(row.worktree, job.repo, job.branch, row.revision, inspection);
  await requireIsolatedWorkspace(job.repo, job.repo, 'main', job.base, inspection);
  const paths = (await inspectGit(row.worktree, job.repo,
    ['diff', '--no-ext-diff', '--no-textconv', '--name-only', job.base, row.revision], inspection)).split('\n').filter(Boolean);
  if (!paths.length || paths.some(path => !job.task.paths.includes(path))) throw new Error('Empty task diff or out-of-scope source changes.');
  row.changed = true;
  row.checks = await verify(row.worktree, job.repo, job.task, { ...options(), image: job.image });
  if (research) {
    const reportCheck = row.checks.executions.find(check => check.command[1] === '/checks/research_report.py');
    const verdict = reportCheck?.stdout.match(/^PASS: structurally valid source report; evidence verdict=(source-feasible|requires-local-proof|blocked)$/m);
    row.evidenceVerdict = verdict?.[1] ?? null;
  }
  await save();
  if (!row.checks.passed) throw new Error('Independent checks failed.');
  // Separate new Codex processes and containers, each with read-only source and Git mounts.
  const reviews = await Promise.allSettled(['standards', 'spec'].map(async axis => {
    const home = join(PRIVATE, 'auth', `${job.id}-${axis}`);
    await mkdir(home, { mode: 0o700 });
    await writeFile(join(home, 'auth.json'), await readFile(join(job.auth, 'auth.json')), { mode: 0o600 });
    const prompt = [
      `Fresh ${axis} review. Review only this axis; source and Git metadata are read-only.`,
      job.skills.review, brief,
      research ? 'This is source-only research. Check immutable citations against the public source, version applicability, fact/inference/unknown separation and every ticket requirement. Structural acceptance cannot establish semantic correctness or runtime readiness.' : '',
      `Pinned diff: git diff --no-ext-diff --no-textconv ${job.base}...${row.revision}. Inspect the complete diff and tests.`,
      axis === 'standards' ? 'Use AGENTS.md, repository conventions and the skill smell baseline. Distinguish hard violations from judgement calls. Skip tooling-enforced findings.' : 'Check every issue requirement for missing/partial behavior, scope creep and incorrect implementation. Cite the requirement for each finding.',
      'The host ran the repository gate and host-selected external acceptance checks successfully. Do not spawn agents or modify files; the host is coordinating the two axes.',
      `End with exactly one <review>{"approved":true,"findings":[],"revision":"${row.revision}"}</review> object. Set approved false and supply actionable findings if needed.`,
    ].join('\n\n');
    const result = await freshReview(axis, row.worktree, job.repo, home, prompt, row.revision,
      { ...options(), image: job.image });
    await writeFile(join(runDir, `${axis}.log`), result.execution.stdout + result.execution.stderr, { mode: 0o600 });
    row.reviews[axis] = result.review;
  }));
  if (reviews.some(result => result.status === 'rejected')) throw new Error('Fresh review session failed.');
  await requireIsolatedWorkspace(row.worktree, job.repo, job.branch, row.revision, { ...options(), image: job.image });
  await requireIsolatedWorkspace(job.repo, job.repo, 'main', job.base, { ...options(), image: job.image });
  row.branchValid = true;
  row.status = acceptResult(row) ? 'accepted' : 'failed';
} catch (error) {
  row.status = controller.signal.aborted ? (cancelled ? 'cancelled' : 'timeout') : 'failed';
  await writeFile(join(runDir, 'error.txt'), String(error.stack ?? error), { mode: 0o600 });
} finally {
  clearTimeout(timer);
  if (sandbox) {
    try { await sandbox.stop(); } catch { row.cleanupError = true; row.status = 'failed'; }
  }
  if (row.worktree) {
    try {
      await preserveWorkspace(row.worktree, job.base, runDir,
        args => inspectGit(row.worktree, job.repo, args, { image: job.image, timeoutMs: 30_000 }));
      row.preservedSource = join(runDir, 'source');
      if (row.status === 'accepted') {
        row.sourceBundle = await exportBranchBundle(row.worktree, job.repo, runDir,
          job.branch, job.base, job.image);
      }
    }
    catch { row.preservationError = true; row.status = 'failed'; }
  }
  row.elapsedSeconds = (performance.now() - started) / 1000;
  await save();
  console.log(`${job.id}: ${row.status}; private evidence ${runDir}`);
  process.stdin.destroy();
  if (row.status !== 'accepted') process.exitCode = 1;
}
