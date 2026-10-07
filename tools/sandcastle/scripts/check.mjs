import { readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { checked } from './process.mjs';
import { TOOL } from './settings.mjs';

for (const dir of ['scripts', 'test', 'integration']) {
  for (const name of await readdir(join(TOOL, dir))) {
    if (!name.endsWith('.mjs')) continue;
    const path = join(TOOL, dir, name);
    await checked(process.execPath, ['--check', path]);
    if (dir === 'test') {
      const output = await checked(process.execPath, [path]);
      console.log(output);
    }
  }
}
console.log('PASS: runner syntax and unit tests');
