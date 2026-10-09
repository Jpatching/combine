import { mkdir, readFile, writeFile, chmod } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { randomUUID, createHash } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { execute, checked } from './process.mjs';
import { parseTaskArgs, requireReadyIssue } from './policy.mjs';
import { authHome, sourceClone, requireWorkspace, gitAt, hostGitEnv } from './workspace.mjs';
import { agentMessage } from './review.mjs';
import { researchInputs, researchFingerprint, requireResearchQualification, recordResearchQualification, beginResearchQualification } from './research.mjs';
import { RESEARCH_QUALIFICATION, TOOL, ROOT, PRIVATE, REPOSITORY, REMOTE, IMAGE, MODEL, EFFORT, PINS, TASKS, LIMIT_MS } from './settings.mjs';

const controller = new AbortController();
process.on('SIGINT', () => controller.abort());
process.on('SIGTERM', () => controller.abort());
const [command, ...args] = process.argv.slice(2);
const options = { signal: controller.signal };
const json = async (path, value) => writeFile(path, JSON.stringify(value, null, 2), { mode: 0o600 });

async function doctor() {
  const node = await checked(process.execPath, ['--version'], options);
  const codex = await checked('codex', ['--version'], options);
  const loginResult = await execute('codex', ['login', 'status'], options);
  const login = loginResult.stdout + loginResult.stderr;
  await checked('docker', ['version', '--format', '{{.Server.Version}}'], options);
  if (node !== `v${PINS.node}` || codex !== `codex-cli ${PINS.codex}` ||
      loginResult.code !== 0 || loginResult.reason || !login.includes('Logged in using ChatGPT')) {
    throw new Error('Pinned Node/Codex and ChatGPT subscription login are required.');
  }
  // Check installed dependency identity without running package code.
  for (const [packageName, expected] of [['@ai-hero/sandcastle', PINS.sandcastle], ['typescript', PINS.typescript]]) {
    const pkg = JSON.parse(await readFile(join(TOOL, 'node_modules', packageName, 'package.json'), 'utf8'));
    if (pkg.version !== expected) throw new Error('Installed dependencies do not match pins. Run npm ci --ignore-scripts.');
  }
  console.log('PASS: pinned tools, Docker access and subscription login');
}

async function imageIdentity() {
  const image = await checked('docker', ['image', 'inspect', IMAGE, '--format', '{{.Id}}'], options);
  const setup = JSON.parse(await readFile(join(PRIVATE, 'setup.json'), 'utf8'));
  if (setup.image !== image) throw new Error('Worker image identity changed; rebuild and rerun smoke.');
  return image;
}

async function buildImage() {
  await doctor();
  const start = performance.now();
  const result = await execute('docker', ['build', '--build-arg', `AGENT_UID=${process.getuid()}`,
    '--build-arg', `AGENT_GID=${process.getgid()}`, '-t', IMAGE, join(TOOL, 'image')],
    { ...options, timeoutMs: 15 * 60_000 });
  await writeFile(join(PRIVATE, 'image-build.log'), result.stdout + result.stderr, { mode: 0o600 });
  if (result.code !== 0 || result.reason) throw new Error('Image build failed; inspect private image-build.log.');
  const image = await checked('docker', ['image', 'inspect', IMAGE, '--format', '{{.Id}}'], options);
  const tools = await checked('docker', ['run', '--rm', '--entrypoint', 'sh', IMAGE,
    '-c', 'node --version && codex --version && python3 --version && git --version'], options);
  if (!tools.includes(`Python ${PINS.python}`) || !tools.includes(`codex-cli ${PINS.codex}`) || !tools.includes(`v${PINS.node}`)) {
    throw new Error('Built image does not contain required pinned tools.');
  }
  await json(join(PRIVATE, 'setup.json'), { image, pins: PINS, tools, buildSeconds: (performance.now() - start) / 1000 });
  console.log(`PASS: image built and tools verified (${image})`);
}

async function smoke() {
  await doctor();
  const image = await imageIdentity();
  const id = `smoke-${randomUUID()}`, home = await authHome(id), name = `combine-${id}`;
  let result;
  try {
    result = await execute('docker', ['run', '--rm', '--name', name,
      '--user', `${process.getuid()}:${process.getgid()}`, '-v', `${home}:/auth`,
      '-e', 'CODEX_HOME=/auth', '--entrypoint', 'codex', image,
      'exec', '--json', '--ephemeral', '--ignore-user-config', '--ignore-rules', '--skip-git-repo-check',
      '-s', 'read-only', '-m', MODEL, '-c', `model_reasoning_effort="${EFFORT}"`,
      'Do not run tools. Respond exactly: COMBINE_AUTH_OK'], { ...options, timeoutMs: 120_000 });
    await writeFile(join(PRIVATE, `${id}.log`), result.stdout + result.stderr, { mode: 0o600 });
    if (result.code !== 0 || result.reason || agentMessage(result.stdout).trim() !== 'COMBINE_AUTH_OK') {
      throw new Error('Subscription/model smoke failed. No API fallback.');
    }
    await json(join(PRIVATE, 'smoke.json'), { passed: true, image, model: MODEL, pins: PINS, at: new Date().toISOString() });
    console.log('PASS: actual subscription inference inside the pinned image');
  } finally {
    await execute('docker', ['rm', '-f', name], { timeoutMs: 20_000 });
  }
}

async function run(qualification = false) {
  const selection = qualification ? { issue: 'qualification', branch: `research/qualification-${randomUUID()}` } : parseTaskArgs(args);
  const task = qualification ? RESEARCH_QUALIFICATION : TASKS[selection.issue];
  if (!task) throw new Error('Issue has no approved host check/scope profile. Add one through a reviewed source slice.');
  const qualificationPath = join(PRIVATE, 'research-smoke.json');
  // A failed new qualification must not leave an earlier candidate qualified.
  if (qualification) await beginResearchQualification(qualificationPath);
  // Resolve supplied skills/guidance before authentication copying or inference.
  const researchSkills = task.kind === 'research' ? await researchInputs() : null;
  await doctor();
  const image = await imageIdentity();
  const smoke = JSON.parse(await readFile(join(PRIVATE, 'smoke.json'), 'utf8'));
  if (!smoke.passed || smoke.image !== image || smoke.model !== MODEL) throw new Error('Run npm run smoke against this image first.');
  const researchIdentity = task.kind === 'research' ? { image, model: MODEL, fingerprint: await researchFingerprint(researchSkills) } : null;
  if (researchIdentity && !qualification) await requireResearchQualification(qualificationPath, researchIdentity);
  const base = await gitAt(ROOT, ['rev-parse', 'main']);
  if (base !== await gitAt(ROOT, ['rev-parse', 'origin/main']) ||
      await gitAt(ROOT, ['remote', 'get-url', 'origin']) !== REMOTE) throw new Error('Synchronize main with Combine origin first.');
  const branch = await gitAt(ROOT, ['branch', '--show-current']);
  if (!qualification && branch !== 'main' && branch !== selection.branch) throw new Error('Chat checkout must be clean main or the exact selected task branch.');
  if (!qualification) await requireWorkspace(ROOT, branch, base);
  const issue = qualification ? { number: 'qualification', title: 'Qualify background public-source research',
    body: 'Using the pinned Universal Modder mashup route and collision guidance, explain why a fixed flat-ground control-transfer proof does not establish arbitrary host-world collision. Inspect the actual public guide files at the pinned commit and cite their source. State one remaining local proof and stop criteria. This is runner qualification only: do not investigate or claim completion of GTA research issues31/32.', comments: [] } : JSON.parse(await checked('gh', ['issue', 'view', String(selection.issue), '--repo', REPOSITORY,
    '--json', 'number,title,body,labels,comments,state'], options));
  if (!qualification) {
  const blockerCount = await checked('gh', ['api', `repos/${REPOSITORY}/issues/${selection.issue}`,
    '--jq', '.issue_dependencies_summary.blocked_by'], options);
  const blocked = /^[0-9]+$/.test(blockerCount) ? Number(blockerCount) : null;
  requireReadyIssue(issue, selection.issue, blocked);
  }
  const id = `issue-${selection.issue}-${randomUUID()}`;
  const runDir = join(PRIVATE, 'runs', id);
  await mkdir(runDir, { recursive: true, mode: 0o700 });
  const started = performance.now();
  const timer = setTimeout(() => controller.abort(), LIMIT_MS);
  timer.unref();
  try {
    const repo = await sourceClone(id, base, controller.signal);
    const auth = await authHome(id);
    const skills = {};
    Object.assign(skills, researchSkills ?? {});
    const skillNames = task.kind === 'research' ? [] : [['implement', 'implement'], ['tdd', 'tdd'], ['review', 'code-review']];
    for (const [key, name] of skillNames) {
      skills[key] = await readFile(join(homedir(), '.codex/skills', name, 'SKILL.md'), 'utf8');
    }
    const lockHash = createHash('sha256').update(await readFile(join(TOOL, 'package-lock.json'))).digest('hex');
    await json(join(runDir, 'job.json'), { id, issue, branch: selection.branch, base, repo, auth, task, skills, image, lockHash, researchIdentity });
    console.log(`Starting one approved issue #${issue.number} on ${selection.branch}; private evidence ${runDir}`);
    const result = await execute(process.execPath, [join(TOOL, 'scripts/worker.mjs'), runDir], {
      cwd: TOOL, env: { PATH: process.env.PATH, HOME: auth, LANG: 'C.UTF-8', TERM: 'dumb', ...hostGitEnv() },
      signal: controller.signal, timeoutMs: Math.max(1, LIMIT_MS - (performance.now() - started)),
      cancellationMessage: 'CANCEL\n', killGraceMs: 45_000,
      onLine: line => { if (line.startsWith(`${id}:`)) console.log(line); },
    });
    await writeFile(join(runDir, 'worker.log'), result.stdout + result.stderr, { mode: 0o600 });
    if (!qualification) await requireWorkspace(ROOT, branch, base);
    const row = JSON.parse(await readFile(join(runDir, 'result.json'), 'utf8'));
    if (result.code !== 0 || result.reason || row.status !== 'accepted') {
      throw new Error(`Task stopped (${row.status}); preserved source/branch and evidence in ${runDir}.`);
    }
    if (qualification) await recordResearchQualification(qualificationPath, researchIdentity, row);
    console.log(`PASS: #${issue.number} checks, fresh Standards/Spec reviews and branch invariants. Host publication remains pending.`);
  } finally { clearTimeout(timer); }
}

try {
  // Parse before creating artifacts, contacting Docker or copying authentication.
  if (command === 'run') parseTaskArgs(args);
  else if (!['doctor', 'build-image', 'smoke', 'research-smoke'].includes(command) || args.length) throw new Error('Commands: doctor, build-image, smoke, research-smoke, run -- --issue <number> --branch <task-branch>');
  await mkdir(PRIVATE, { recursive: true, mode: 0o700 });
  await chmod(PRIVATE, 0o700);
  if (command === 'doctor') await doctor();
  else if (command === 'build-image') await buildImage();
  else if (command === 'smoke') await smoke();
  else if (command === 'research-smoke') await run(true);
  else await run();
} catch (error) {
  // Print only bounded, coordinator-authored errors; detailed child output belongs privately.
  await mkdir(PRIVATE, { recursive: true, mode: 0o700 });
  await writeFile(join(PRIVATE, 'coordinator-error.txt'), String(error.stack ?? error), { mode: 0o600 });
  console.error(error.message?.startsWith('Task stopped') ? error.message : 'FAIL: setup or task precondition failed; check tools, approved issue, checkout and private evidence.');
  process.exitCode = 1;
}
