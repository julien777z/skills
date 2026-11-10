#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { inspect, isDeepStrictEqual, parseArgs, parseEnv } from 'node:util';
import { cancellation, secretValues, withT3Session } from '../resources/session.mjs';

const VARIABLE_NAME = /^[a-zA-Z_][a-zA-Z0-9_]{0,127}$/;
const COMMANDS = new Set(['list', 'merge', 'set', 'unset']);

function printHelp() {
  console.log(`Usage: node env.mjs COMMAND [NAMES...] [OPTIONS]

Commands:
  list                  List provider IDs and variable names; never values
  merge                 Merge dotenv or JSON string-map input
  set NAME              Set one literal value from stdin or --file
  unset NAME ...        Remove only the named variables

Options:
  --provider ID         Target provider instance; repeat for several
  --file PATH           Read supplied data from a file; default stdin (-)
  --format auto|dotenv|json  Input format for merge (default auto)
  --apply               Apply changes; otherwise print a name-only preview
  --ssh USER@HOST       Manage T3 through an existing SSH connection
  --identity PATH       Existing SSH identity file
  --known-hosts PATH    Existing SSH known-hosts file
  --base-dir PATH       T3 data directory on the target (default T3CODE_HOME or ~/.t3)
  --t3 PATH             Installed CLI executable on the target (default t3)
  --expect-environment ID  Refuse a different execution environment
  --help                Show this help

Requires Node.js 22+, an installed T3 CLI and a running target server.
Values are supplied as data, never as command arguments. Imports are sensitive.`);
}

function parseCommand() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      provider: { type: 'string', multiple: true },
      file: { type: 'string', default: '-' },
      format: { type: 'string', default: 'auto' },
      apply: { type: 'boolean', default: false },
      ssh: { type: 'string' },
      identity: { type: 'string' },
      'known-hosts': { type: 'string' },
      'base-dir': { type: 'string' },
      t3: { type: 'string', default: 't3' },
      'expect-environment': { type: 'string' },
      help: { type: 'boolean', default: false },
    },
  });

  if (values.help) return { help: true };

  const [command, ...names] = positionals;

  if (!COMMANDS.has(command)) throw new Error('Choose list, merge, set or unset; see --help.');
  if (!['auto', 'dotenv', 'json'].includes(values.format)) throw new Error('Unknown input format.');
  if (command === 'set' && names.length !== 1) throw new Error('set requires one variable name.');
  if (command === 'unset' && names.length === 0) throw new Error('unset requires variable names.');
  if (['list', 'merge'].includes(command) && names.length) throw new Error('Unexpected variable names.');

  for (const name of names) {
    if (!VARIABLE_NAME.test(name)) throw new Error(`Invalid variable name: ${name}`);
  }

  const providers = [...new Set(values.provider ?? [])];

  if (command !== 'list' && providers.length === 0) throw new Error('Select at least one --provider ID.');
  if (!values.ssh && (values.identity || values['known-hosts'])) throw new Error('SSH file options require --ssh.');

  return { ...values, command, names, providers };
}

async function readInput(options) {
  if (!['merge', 'set'].includes(options.command)) return new Map();
  if (options.file === '-' && process.stdin.isTTY) throw new Error('Pipe input or supply --file PATH.');

  const chunks = [];

  if (options.file === '-') {
    for await (const chunk of process.stdin) chunks.push(Buffer.from(chunk));
  } else {
    chunks.push(await readFile(options.file));
  }

  const input = Buffer.concat(chunks).toString('utf8');

  if (options.command === 'set') {
    secretValues.add(input);

    return new Map([[options.names[0], input]]);
  }

  const format = options.format === 'auto'
    ? (input.trimStart().startsWith('{') ? 'json' : 'dotenv')
    : options.format;
  const parsed = format === 'json' ? JSON.parse(input) : parseEnv(input);

  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error('Input must be dotenv text or a JSON object of string values.');
  }

  const entries = Object.entries(parsed);

  for (const [name, value] of entries) {
    if (typeof value === 'string') secretValues.add(value);
    if (!VARIABLE_NAME.test(name)) throw new Error(`Invalid variable name: ${name}`);
    if (typeof value !== 'string') throw new Error(`Environment value for ${name} must be a string.`);
  }

  if (!entries.length) throw new Error('Input contains no variable assignments.');

  return new Map(entries);
}

function mergeInstance(instance, incoming, options) {
  const environment = new Map((instance.environment ?? []).map((variable) => [variable.name, variable]));

  if (options.command === 'unset') {
    for (const name of options.names) environment.delete(name);
  } else {
    for (const [name, value] of incoming) environment.set(name, { name, value, sensitive: true });
  }

  return { ...instance, environment: [...environment.values()] };
}

async function run(options, incoming) {
  const scopes = ['orchestration:read'];

  if (options.command !== 'list' && options.apply) scopes.push('providers:manage');

  await withT3Session({ ...options, scopes }, async (rpc) => {
    const config = await rpc('server.getConfig');
    let settings = await rpc('server.getSettings');
    const environment = config.environment;

    if (options['expect-environment'] && environment.environmentId !== options['expect-environment']) {
      throw new Error(`Wrong T3 environment: ${environment.environmentId} (${environment.label}).`);
    }

    const available = new Map(config.providers.map((provider) => [provider.instanceId, provider]));
    const selected = options.providers.length ? options.providers : [...available.keys()];

    for (const id of selected) {
      if (!available.has(id)) throw new Error(`Unknown provider instance: ${id}`);
    }

    const summary = selected.map((id) => {
      const provider = available.get(id);
      const current = settings.providerInstances[id] ?? { driver: provider.driver };
      const names = (current.environment ?? []).map((variable) => variable.name);

      return { id, name: provider.displayName ?? id, driver: provider.driver, variables: names,
        ...(options.command === 'list' ? {} : {
          add: [...incoming.keys()].filter((name) => !names.includes(name)),
          update: [...incoming.keys()].filter((name) => names.includes(name)),
          remove: options.command === 'unset' ? options.names.filter((name) => names.includes(name)) : [],
        }) };
    });
    console.log(JSON.stringify({ environment: { id: environment.environmentId, label: environment.label,
      version: environment.serverVersion }, apply: options.apply, providers: summary }, null, 2));

    if (options.command !== 'list' && options.apply) {
      for (const id of selected) {
        settings = await rpc('server.getSettings');
        const current = settings.providerInstances[id] ?? { driver: available.get(id).driver };
        const next = mergeInstance(current, incoming, options);
        await rpc('server.updateSettings', { patch: {},
          providerInstanceMutation: { operation: 'upsert', instanceId: id, instance: next } });
        const verified = await rpc('server.getSettings');
        const actual = verified.providerInstances[id];
        const expectedNames = next.environment.map((variable) => variable.name);
        const actualNames = (actual?.environment ?? []).map((variable) => variable.name);

        if (JSON.stringify(expectedNames) !== JSON.stringify(actualNames)) {
          throw new Error(`Provider ${id} variable readback differs from the requested change.`);
        }

        for (const name of incoming.keys()) {
          const value = actual.environment.find((variable) => variable.name === name);
          const input = incoming.get(name);
          const redacted = value?.valueRedacted === true;
          const emptySensitiveValue = input === '' && value?.value === '';

          if (value?.sensitive !== true || (!redacted && !emptySensitiveValue)) {
            throw new Error(`Provider ${id} did not retain ${name} as a configured secret.`);
          }
        }

        const touched = new Set(options.command === 'unset' ? options.names : incoming.keys());

        for (const previous of current.environment ?? []) {
          if (touched.has(previous.name)) continue;

          const retained = actual.environment.find((variable) => variable.name === previous.name);

          if (!isDeepStrictEqual(previous, retained)) {
            throw new Error(`Provider ${id} unrelated variable ${previous.name} changed.`);
          }
        }

        const { environment: oldEnvironment, ...oldFields } = current;
        const { environment: actualEnvironment, ...actualFields } = actual;

        if (!isDeepStrictEqual(oldFields, actualFields)) {
          throw new Error(`Provider ${id} unrelated settings changed during readback.`);
        }

        console.log(JSON.stringify({ verified: id, variables: actualNames }));
      }
    }
  });
}

function redact(error) {
  let message = inspect(error, { depth: null });
  const variants = [...secretValues].filter((value) => typeof value === 'string' && value.length)
    .flatMap((value) => [value, JSON.stringify(value).slice(1, -1)])
    .sort((left, right) => right.length - left.length);

  for (const value of variants) message = message.replaceAll(value, '[REDACTED]');

  message = message.replace(/"[^"\n]*"(?:\.\.\.)?(?= is not valid JSON)/g, '[REDACTED input]');

  return message;
}

process.once('SIGINT', () => cancellation.abort(new Error('Interrupted.')));
process.once('SIGTERM', () => cancellation.abort(new Error('Terminated.')));

try {
  if (Number(process.versions.node.split('.')[0]) < 22) throw new Error('Node.js 22 or newer is required.');

  const options = parseCommand();

  if (options.help) printHelp();
  else await run(options, await readInput(options));
} catch (error) {
  console.error(redact(error));
  process.exitCode = 1;
}
