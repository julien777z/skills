# Container Runtime

Contents: **macOS**, **Linux**, **Reporting unavailable**.

How `run-site`'s **Start and verify the stack** starts the container runtime and when it reports
Docker unavailable.

## macOS

- **Use OrbStack for local containers when it is installed.** Before starting container-backed
  work for any application on macOS, check whether OrbStack is installed even if the current Docker
  context points elsewhere. Start OrbStack if it is stopped, then verify that Docker can reach its
  engine. Use the OrbStack context for Docker and Compose. Pass it through `DOCKER_CONTEXT` when an
  application launcher invokes those commands, then verify the containers are running in OrbStack.
  If its engine is unavailable, diagnose startup and context selection without falling back to
  Docker Desktop. When OrbStack is absent, follow the host's configured container runtime.

## Linux

- On Linux, prefer the repository's service-startup helper or skill. Otherwise start the daemon
  explicitly and wait for `docker info` to succeed:

```bash
mkdir -p .agent_sources/logs
sudo systemctl start docker 2>/dev/null \
  || sudo service docker start 2>/dev/null \
  || (sudo dockerd > .agent_sources/logs/dockerd.log 2>&1 & disown)

for attempt in $(seq 1 15); do
  docker info > /dev/null 2>&1 && break
  sleep 1
done
```

## Reporting unavailable

- Report Docker as unavailable only when the CLI is missing or `docker info` still fails after the explicit start attempt, and include the daemon log in that report.
