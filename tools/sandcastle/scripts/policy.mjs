export function parseTaskArgs(args) {
  const values = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i];
    if (!['--issue', '--branch'].includes(key) || values[key] || !args[i + 1]) {
      throw new Error('Usage: npm run run -- --issue <number> --branch <task-branch>');
    }
    values[key] = args[i + 1];
  }
  const branch = values['--branch'] ?? '';
  if (!/^[1-9][0-9]*$/.test(values['--issue'] ?? '') ||
      !/^[a-z][a-z0-9-]*\/[a-zA-Z0-9][a-zA-Z0-9/_-]*$/.test(branch) ||
      branch.endsWith('/') || branch.includes('//')) {
    throw new Error('Provide a positive issue number and a named task branch (for example fix/markdown-links).');
  }
  const issue = Number(values['--issue']);
  if (!Number.isSafeInteger(issue)) throw new Error('Invalid issue number.');
  return { issue, branch };
}

export function requireReadyIssue(issue, expected, blocked) {
  if (issue.number !== expected || issue.state !== 'OPEN' ||
      !issue.labels.some(label => label.name === 'ready-for-agent') || blocked !== 0) {
    throw new Error('Selected issue must be open, ready-for-agent and have no open blockers.');
  }
  if (!issue.body?.trim() || !Array.isArray(issue.comments)) throw new Error('Incomplete issue brief.');
}

export function acceptResult(result) {
  return Boolean((result.kind !== 'research' || (result.researcherCompleted === true &&
    ['source-feasible', 'requires-local-proof', 'blocked'].includes(result.evidenceVerdict))) && result.branchValid && result.changed && result.checks?.passed &&
    result.checks.revision === result.revision &&
    ['standards', 'spec'].every(axis => {
      const review = result.reviews?.[axis];
      return review?.approved === true && Array.isArray(review.findings) &&
        review.findings.length === 0 && review.revision === result.revision;
    }));
}

export function parseReview(text, revision) {
  const matches = [...text.matchAll(/<review>([^]*?)<\/review>/g)];
  if (matches.length !== 1) throw new Error('Reviewer must supply exactly one structured review.');
  const review = JSON.parse(matches[0][1]);
  if (typeof review.approved !== 'boolean' || !Array.isArray(review.findings) ||
      review.revision !== revision) throw new Error('Review has an invalid verdict or revision.');
  return review;
}
