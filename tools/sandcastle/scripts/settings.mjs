import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

export const TOOL = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const ROOT = resolve(TOOL, '../..');
export const PRIVATE = join(ROOT, '.private/sandcastle');
export const REPOSITORY = 'Jpatching/combine';
export const REMOTE = 'https://github.com/Jpatching/combine.git';
export const IMAGE = 'combine-sandcastle:0.12.0-codex-0.160.1-python-3.10';
export const MODEL = 'gpt-6.1-sol';
export const EFFORT = 'medium';
export const LIMIT_MS = 30 * 60 * 1000;
export const PINS = { sandcastle: '0.12.0', codex: '0.160.1', node: '24.10.0', typescript: '6.0.3', python: '3.10.19' };

// These checks are reviewed host configuration, never commands from issue text.
export const TASKS = {
  12: {
    paths: ['scripts/verify.py', 'tests/test_doc_links.py'],
    checks: [['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_doc_links.py', '-v'],
      ['python3', '/checks/markdown_links.py']],
  },
};
