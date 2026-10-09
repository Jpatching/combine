import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execute } from '../scripts/process.mjs';
import { TOOL } from '../scripts/settings.mjs';

const revision = 'a'.repeat(40);
const url = `https://github.com/owner/source/blob/${revision}/query.cpp`;
const report = `# Collision feasibility\n\n## Verified source facts\nSource has a query. [Implementation](${url}).\n\n## Source inference\nIts port needs validation.\n\n## Unknowns\nExact game behavior remains unknown.\n\n## Next local proof\nObserve a floor and a miss.\n\n<research>${JSON.stringify({ verdict: 'requires-local-proof', runtimeVerified: false, sources: [{ url, revision }], inaccessibleSources: [], unknowns: ['Exact game behavior'] })}</research>\n`;

test('report acceptance requires a bounded source-only report with immutable citations and honest verdict', async t => {
  const root = await mkdtemp(join(tmpdir(), 'combine-research-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  await mkdir(join(root, 'research/results'), { recursive: true });
  const path = 'research/results/report.md';
  const check = () => execute('python3', [join(TOOL, 'acceptance/research_report.py'), path], { cwd: root });
  await writeFile(join(root, path), report);
  assert.equal((await check()).code, 0);
  for (const invalid of [report.replace(revision, 'main'), report.replace('"runtimeVerified":false', '"runtimeVerified":true'), report.replace('requires-local-proof', 'gameplay-verified'), report.replace('## Unknowns', '## Omitted'), report.replace(`[Implementation](${url}).`, ''), report + '\n<research>{}</research>', 'x'.repeat(65537)]) {
    await writeFile(join(root, path), invalid);
    assert.notEqual((await check()).code, 0);
  }
  await rm(join(root, path));
  await writeFile(join(root, 'outside.md'), report);
  await symlink(join(root, 'outside.md'), join(root, path));
  assert.notEqual((await check()).code, 0);
});

import { acceptResult } from '../scripts/policy.mjs';

test('research acceptance needs completed delegated research and an evidence verdict as well as two reviews', () => {
  const review = { approved: true, findings: [], revision: 'abc' };
  const row = { kind: 'research', revision: 'abc', checks: { passed: true, revision: 'abc' },
    reviews: { standards: review, spec: review }, branchValid: true, changed: true };
  assert.equal(acceptResult(row), false);
  assert.equal(acceptResult({ ...row, researcherCompleted: true, evidenceVerdict: 'requires-local-proof' }), true);
  assert.equal(acceptResult({ ...row, researcherCompleted: true, evidenceVerdict: 'runtime-proven' }), false);
});

import { recordResearchQualification, requireResearchQualification, beginResearchQualification, researchFingerprint } from '../scripts/research.mjs';

test('production research requires an accepted qualification matching image, model and complete input fingerprint', async t => {
  const root = await mkdtemp(join(tmpdir(), 'combine-qualified-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const path = join(root, 'qualification.json');
  const expected = { image: 'sha256:image', model: 'pinned-model', fingerprint: 'a'.repeat(64) };
  await assert.rejects(requireResearchQualification(path, expected));
  await assert.rejects(recordResearchQualification(path, expected, { status: 'failed' }));
  await assert.rejects(requireResearchQualification(path, expected));
  const review = { approved: true, findings: [], revision: 'abc' };
  const row = { kind: 'research', issue: 'qualification', researcherCompleted: true,
    evidenceVerdict: 'requires-local-proof', status: 'accepted', revision: 'abc',
    checks: { passed: true, revision: 'abc' }, reviews: { standards: review, spec: review }, branchValid: true, changed: true };
  await recordResearchQualification(path, expected, row);
  await assert.doesNotReject(requireResearchQualification(path, expected));
  for (const stale of [{ ...expected, image: 'different' }, { ...expected, model: 'different' }, { ...expected, fingerprint: 'b'.repeat(64) }]) {
    await assert.rejects(requireResearchQualification(path, stale));
  }
  await beginResearchQualification(path);
  await assert.rejects(recordResearchQualification(path, expected, { ...row, status: 'failed' }));
  await assert.rejects(requireResearchQualification(path, expected));
  await writeFile(path, JSON.stringify({ ...expected, passed: false }));
  await assert.rejects(requireResearchQualification(path, expected));
});

test('research fingerprint changes with supplied skill and guidance changes', async () => {
  const first = await researchFingerprint({ research: 'original skill', guidance: ['pinned text'], review: 'original review' });
  assert.equal(await researchFingerprint({ research: 'original skill', guidance: ['pinned text'], review: 'original review' }), first);
  assert.notEqual(await researchFingerprint({ research: 'changed skill', guidance: ['pinned text'], review: 'original review' }), first);
  assert.notEqual(await researchFingerprint({ research: 'original skill', guidance: ['changed text'], review: 'original review' }), first);
  assert.notEqual(await researchFingerprint({ research: 'original skill', guidance: ['pinned text'], review: 'changed review' }), first);
});
