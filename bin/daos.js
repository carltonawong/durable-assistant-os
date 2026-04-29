#!/usr/bin/env node
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const packageRoot = path.resolve(__dirname, '..');
const pythonScript = path.join(packageRoot, 'scripts', 'daos.py');

function candidateCommands() {
  if (process.env.DAOS_PYTHON) {
    return [[process.env.DAOS_PYTHON, []]];
  }
  return [
    ['python3', []],
    ['py', ['-3']],
    ['python', []],
  ];
}

function probePython(command, prefixArgs) {
  const result = spawnSync(command, [
    ...prefixArgs,
    '-c',
    'import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)',
  ], {
    encoding: 'utf8',
    windowsHide: true,
  });
  if (result.error) {
    return false;
  }
  return result.status === 0;
}

function findPython() {
  for (const [command, prefixArgs] of candidateCommands()) {
    if (probePython(command, prefixArgs)) {
      return { command, prefixArgs };
    }
  }
  return null;
}

function main() {
  if (!fs.existsSync(pythonScript)) {
    process.stderr.write(`DAOS package is missing its Python entrypoint: ${pythonScript}\n`);
    return 1;
  }

  const python = findPython();
  if (!python) {
    process.stderr.write('DAOS needs Python 3 to run this preview build.\n');
    process.stderr.write('Install Python 3, then run: npx daos init\n');
    return 1;
  }

  const interactive = Boolean(process.stdin.isTTY);
  const result = spawnSync(
    python.command,
    [...python.prefixArgs, pythonScript, ...process.argv.slice(2)],
    {
      cwd: process.cwd(),
      env: process.env,
      encoding: 'utf8',
      stdio: interactive ? 'inherit' : ['pipe', 'pipe', 'pipe'],
      windowsHide: true,
    }
  );

  if (result.error) {
    process.stderr.write(`DAOS failed to start Python: ${result.error.message}\n`);
    return 1;
  }
  if (result.stdout) {
    process.stdout.write(result.stdout);
  }
  if (result.stderr) {
    process.stderr.write(result.stderr);
  }
  return result.status === null ? 1 : result.status;
}

process.exitCode = main();
