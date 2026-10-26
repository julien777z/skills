#!/usr/bin/env node
import { execFile, spawn } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { resolve } from 'node:path';
import { createServer, connect } from 'node:net';
import { setTimeout as delay } from 'node:timers/promises';
import { inspect, isDeepStrictEqual, parseArgs, parseEnv, promisify } from 'node:util';

const execute = promisify(execFile);
const VARIABLE_NAME = /^[a-zA-Z_][a-zA-Z0-9_]{0,127}$/;
const COMMANDS = new Set(['list', 'merge', 'set', 'unset']);
const TIMEOUT_MS = 15_000;
const secretValues = new Set();
const cancellation = new AbortController();
const metadataProgram = `
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const baseDir = path.resolve(process.argv[1] || process.env.T3CODE_HOME || path.join(os.homedir(), '.t3'));
const runtime = JSON.parse(fs.readFileSync(path.join(baseDir, 'userdata/server-runtime.json'), 'utf8'));
process.stdout.write(JSON.stringify({ baseDir, origin: runtime.origin }));
`;

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

function sshArguments(options) {
  const args = ['-T', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10'];

  if (options.identity) args.push('-i', options.identity, '-o', 'IdentitiesOnly=yes');
  if (options['known-hosts']) args.push('-o', `UserKnownHostsFile=${options['known-hosts']}`);

  return args;
}

function shellQuote(value) {
  return `'${String(value).replaceAll("'", "'\\''")}'`;
}

async function targetCommand(options, command, args, cleanup = false) {
  const invocation = options.ssh
    ? {
      command: 'ssh',
      args: [...sshArguments(options), '--', options.ssh,
        `PATH="$HOME/.local/bin:$PATH" ${[command, ...args].map(shellQuote).join(' ')}`],
    }
    : { command, args };
  const { stdout } = await execute(invocation.command, invocation.args, {
    timeout: TIMEOUT_MS,
    maxBuffer: 2 * 1024 * 1024,
    ...(cleanup ? {} : { signal: cancellation.signal }),
  });

  return stdout;
}

async function openForward(options, remoteOrigin) {
  const reservation = createServer();
  await new Promise((accept, reject) => {
    reservation.once('error', reject);
    reservation.listen(0, '127.0.0.1', accept);
  });
  const port = reservation.address().port;
  await new Promise((accept, reject) => reservation.close((error) => error ? reject(error) : accept()));

  const tunnel = spawn('ssh', [...sshArguments(options), '-N', '-o', 'ExitOnForwardFailure=yes',
    '-L', `127.0.0.1:${port}:${remoteOrigin.hostname}:${remoteOrigin.port || '80'}`,
    '--', options.ssh], { stdio: ['ignore', 'ignore', 'pipe'] });
  let diagnostic = '';
  let startupError;
  tunnel.stderr.on('data', (chunk) => { diagnostic += chunk.toString(); });
  tunnel.once('error', (error) => { startupError = error; });

  try {
    const deadline = Date.now() + TIMEOUT_MS;

    while (Date.now() < deadline) {
      cancellation.signal.throwIfAborted();
      if (startupError) throw startupError;
      if (tunnel.exitCode !== null) throw new Error(`SSH forwarding failed: ${diagnostic}`);

      const ready = await new Promise((accept) => {
        const probe = connect({ host: '127.0.0.1', port });
        probe.once('connect', () => { probe.destroy(); accept(true); });
        probe.once('error', () => { probe.destroy(); accept(false); });
      });

      if (ready) return { tunnel, origin: new URL(`http://127.0.0.1:${port}`) };

      await delay(50, undefined, { signal: cancellation.signal });
    }

    throw new Error(`SSH forwarding timed out: ${diagnostic}`);
  } catch (error) {
    tunnel.kill('SIGTERM');

    throw error;
  }
}

async function openRpc(origin, token) {
  const ticketResponse = await fetch(new URL('/api/auth/websocket-ticket/rpc', origin), {
    method: 'POST',
    headers: { authorization: `Bearer ${token}` },
    signal: AbortSignal.any([cancellation.signal, AbortSignal.timeout(TIMEOUT_MS)]),
  });
  const ticketBody = await ticketResponse.text();

  if (!ticketResponse.ok) throw new Error(`T3 ticket request failed (${ticketResponse.status}): ${ticketBody}`);

  const { ticket } = JSON.parse(ticketBody);

  if (typeof ticket !== 'string' || !ticket) throw new Error('T3 returned an invalid WebSocket ticket.');

  secretValues.add(ticket);
  const url = new URL('/ws', origin);
  url.protocol = origin.protocol === 'https:' ? 'wss:' : 'ws:';
  url.searchParams.set('orchestrationProtocol', '2');
  url.searchParams.set('wsTicket', ticket);

  const socket = new WebSocket(url);
  const pending = new Map();
  let requestId = 0;
  const failPending = (error) => {
    for (const request of pending.values()) {
      clearTimeout(request.timer);
      request.reject(error);
    }
    pending.clear();
  };
  socket.addEventListener('close', () => failPending(new Error('T3 RPC socket closed before its result.')));
  socket.addEventListener('error', (event) => failPending(new Error('T3 WebSocket transport failed.', { cause: event.error })));
  socket.addEventListener('message', (event) => {
    try {
      const message = JSON.parse(event.data);

      if (message._tag === 'Ping') {
        socket.send(JSON.stringify({ _tag: 'Pong' }));

        return;
      }
      if (message._tag === 'Pong') return;
      if (message._tag === 'Defect') throw new Error(`T3 RPC defect: ${JSON.stringify(message)}`);
      if (message._tag !== 'Exit') throw new Error(`Unexpected T3 RPC envelope: ${JSON.stringify(message)}`);

      const request = pending.get(message.requestId);

      if (!request) throw new Error(`T3 returned an unknown request ID: ${message.requestId}`);

      clearTimeout(request.timer);
      pending.delete(message.requestId);

      if (message.exit?._tag === 'Success') request.resolve(message.exit.value);
      else request.reject(new Error(`T3 ${request.method} failed: ${JSON.stringify(message.exit)}`));
    } catch (error) {
      failPending(error);
      socket.close();
    }
  });

  try {
    await new Promise((accept, reject) => {
      const timer = setTimeout(() => reject(new Error('T3 WebSocket handshake timed out.')), TIMEOUT_MS);
      socket.addEventListener('open', () => { clearTimeout(timer); accept(); }, { once: true });
      socket.addEventListener('error', (event) => {
        clearTimeout(timer);
        reject(new Error('T3 WebSocket handshake failed.', { cause: event.error }));
      }, { once: true });
    });
  } catch (error) {
    socket.close();

    throw error;
  }

  return {
    close: () => socket.close(),
    call(method, payload = {}) {
      return new Promise((accept, reject) => {
        const id = ++requestId;
        const timer = setTimeout(() => {
          pending.delete(id);
          reject(new Error(`T3 ${method} timed out.`));
        }, TIMEOUT_MS);
        pending.set(id, { resolve: accept, reject, timer, method });
        socket.send(JSON.stringify({ _tag: 'Request', id, tag: method, payload, headers: [] }));
      });
    },
  };
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
  let rpc;
  let tunnel;
  let session;
  let failure;
  let metadata;

  try {
    metadata = JSON.parse(await targetCommand(options, options.ssh ? 'node' : process.execPath,
      ['-e', metadataProgram, options['base-dir'] ?? '']));
    const origin = new URL(metadata.origin);

    if (origin.protocol !== 'http:' || !['127.0.0.1', 'localhost', '[::1]'].includes(origin.hostname)) {
      throw new Error('The running T3 origin must be its local HTTP listener.');
    }

    let connectionOrigin = origin;

    if (options.ssh) {
      const forward = await openForward(options, origin);
      tunnel = forward.tunnel;
      connectionOrigin = forward.origin;
    }

    const scopes = ['--scope', 'orchestration:read'];

    if (options.command !== 'list' && options.apply) scopes.push('--scope', 'providers:manage');

    session = JSON.parse(await targetCommand(options, options.t3, ['auth', 'session', 'issue',
      '--base-dir', metadata.baseDir, '--json', '--ttl', '5m', '--label', 't3-code env', ...scopes]));
    secretValues.add(session.token);
    rpc = await openRpc(connectionOrigin, session.token);
    const config = await rpc.call('server.getConfig');
    let settings = await rpc.call('server.getSettings');
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
        settings = await rpc.call('server.getSettings');
        const current = settings.providerInstances[id] ?? { driver: available.get(id).driver };
        const next = mergeInstance(current, incoming, options);
        await rpc.call('server.updateSettings', { patch: {},
          providerInstanceMutation: { operation: 'upsert', instanceId: id, instance: next } });
        const verified = await rpc.call('server.getSettings');
        const actual = verified.providerInstances[id];
        const expectedNames = next.environment.map((variable) => variable.name);
        const actualNames = (actual?.environment ?? []).map((variable) => variable.name);

        if (JSON.stringify(expectedNames) !== JSON.stringify(actualNames)) {
          throw new Error(`Provider ${id} variable readback differs from the requested change.`);
        }

        for (const name of incoming.keys()) {
          const value = actual.environment.find((variable) => variable.name === name);

          if (value?.sensitive !== true || value?.valueRedacted !== true) {
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
  } catch (error) {
    failure = error;
  } finally {
    rpc?.close();
    tunnel?.kill('SIGTERM');

    if (session?.sessionId) {
      try {
        await targetCommand(options, options.t3, ['auth', 'session', 'revoke', session.sessionId,
          '--base-dir', metadata.baseDir], true);
      } catch (error) {
        failure = failure ? new AggregateError([failure, error], 'T3 operation and session cleanup failed.') : error;
      }
    }
  }

  if (failure) throw failure;
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
