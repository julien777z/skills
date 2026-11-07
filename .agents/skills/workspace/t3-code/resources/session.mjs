import { execFile, spawn } from 'node:child_process';
import { createServer, connect } from 'node:net';
import { setTimeout as delay } from 'node:timers/promises';
import { promisify } from 'node:util';

const execute = promisify(execFile);
const TIMEOUT_MS = 15_000;
export const secretValues = new Set();
export const cancellation = new AbortController();
const metadataProgram = `
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const baseDir = path.resolve(process.argv[1] || process.env.T3CODE_HOME || path.join(os.homedir(), '.t3'));
const runtime = JSON.parse(fs.readFileSync(path.join(baseDir, 'userdata/server-runtime.json'), 'utf8'));
process.stdout.write(JSON.stringify({ baseDir, origin: runtime.origin }));
`;

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

export async function withT3Session(options, callback) {
  options = { t3: 't3', ...options };
  let rpc;
  let tunnel;
  let session;
  let failure;
  let metadata;
  let result;

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

    const scopes = (options.scopes ?? ['orchestration:read']).flatMap((scope) => ['--scope', scope]);

    session = JSON.parse(await targetCommand(options, options.t3, ['auth', 'session', 'issue',
      '--base-dir', metadata.baseDir, '--json', '--ttl', '5m', '--label', 't3-code env', ...scopes]));
    secretValues.add(session.token);
    rpc = await openRpc(connectionOrigin, session.token);
    result = await callback((method, payload) => rpc.call(method, payload));
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

  return result;
}
