import test from 'node:test';
import assert from 'node:assert/strict';
import { parseTaskArgs, requireReadyIssue, acceptResult, parseReview } from '../scripts/policy.mjs';

test('task command requires one explicit issue and task branch', () => {
  assert.deepEqual(parseTaskArgs(['--issue', '12', '--branch', 'fix/markdown-links']),
    { issue: 12, branch: 'fix/markdown-links' });
  for (const args of [[], ['--issue', '12'], ['--issue', '12', '--branch', 'main'],
    ['--issue', '0', '--branch', 'fix/x'], ['--issue', '12', '--branch', '../escape'],
    ['--issue', '12', '--branch', 'fix/x', '--issue', '13']]) {
    assert.throws(() => parseTaskArgs(args));
  }
});

test('review must provide one honest verdict for the checked revision', () => {
  assert.equal(parseReview('<review>{"approved":true,"findings":[],"revision":"abc"}</review>', 'abc').approved, true);
  for (const text of ['', '<review>{"approved":true,"findings":[],"revision":"other"}</review>',
    '<review>{"approved":"yes","revision":"abc"}</review>',
    '<review>{"approved":true,"findings":[],"revision":"abc"}</review><review>{}</review>']) {
    assert.throws(() => parseReview(text, 'abc'));
  }
});

test('only the explicit open ready issue with resolved blockers can run', () => {
  const issue = { number: 12, state: 'OPEN', labels: [{ name: 'ready-for-agent' }],
    body: 'Approved task', comments: [] };
  assert.doesNotThrow(() => requireReadyIssue(issue, 12, 0));
  for (const [candidate, blocked] of [[{ ...issue, number: 13 }, 0],
    [{ ...issue, state: 'CLOSED' }, 0], [{ ...issue, labels: [] }, 0], [issue, 1]]) {
    assert.throws(() => requireReadyIssue(candidate, 12, blocked));
  }
});

test('acceptance requires both reviews and checks at the unchanged final revision', () => {
  const review = { approved: true, findings: [], revision: 'abc' };
  const result = { revision: 'abc', checks: { passed: true, revision: 'abc' },
    reviews: { standards: review, spec: review }, branchValid: true, changed: true };
  assert.equal(acceptResult(result), true);
  for (const failed of [{ ...result, checks: { passed: false, revision: 'abc' } },
    { ...result, revision: 'def' }, { ...result, branchValid: false },
    { ...result, changed: false }, { ...result, reviews: { standards: review } },
    { ...result, reviews: { standards: review, spec: { ...review, findings: ['bug'] } } }]) {
    assert.equal(acceptResult(failed), false);
  }
});
