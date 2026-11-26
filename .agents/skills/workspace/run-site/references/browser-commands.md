# Browser Commands

Contents: **Symptoms**, **Sign in**, **Drive the change**, **Widths and full-page captures**.

The commands and the table `run-site` points to; the rules that say when and why stay in its entry
point.

## Symptoms

| Symptom | Likely cause | Fix at the owner |
|---|---|---|
| Every authenticated request returns 401 | A checked-in placeholder shadowed the real value from the session environment | Make the environment win over the dotenv layers; read the running process's environment to confirm |
| A service starts but every query fails | The database has no schemas | Run schema provisioning before launch and read its output for the failing service |
| A module is missing at import though the manifest names it | It is declared where the package manager does not install it | Declare it in the manifest's install list, regenerate the lock, and install; never patch the environment by hand |
| A setup command reports missing settings before doing anything | Import-time application config | Import only what build tooling needs, and keep a test guarding it |
| A `run`-style script reports command not found | Entry point registered only by an install | Invoke bootstrap commands as modules so they need no registration |
| A dependency service refuses connections | It is not in the started set | Start it through the launcher's service selection |
| The browser reaches loopback but no external host | The egress relay accepts only HTTPS CONNECT tunnels | Bypass the proxy for loopback in the browser configuration |
| The browser fails with a connection reset where `curl` succeeds | An inspecting proxy resets the browser's TLS 1.3 handshake | Cap the browser's TLS version in its configuration; never read this as no browser egress |
| Signed in, but mutations no-op and the console reports a cookie failure | The page is not a secure context, so `crypto.subtle` is undefined | Serve and browse on `localhost`, not a wildcard bind address |
| A click reports success and no request follows | The ref resolved but the event never reached the handler | Click the element through `eval` and confirm the request in the service log |

## Sign in

```bash
SIGN_IN_PASSWORD="$(cat <password-file>)" python3 - <<'EOF' | agent-browser --session <name> eval --stdin
import json, os
secret = os.environ["SIGN_IN_PASSWORD"]
js = ("const el=document.querySelector('input[type=\"password\"]');"
      "Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,%s);"
      "el.dispatchEvent(new Event('input',{bubbles:true}));'ok'") % json.dumps(secret)
print(js)
EOF
```

## Drive the change

```bash
agent-browser --session <name> mouse move <x> <y>
agent-browser --session <name> mouse down
agent-browser --session <name> mouse move <x2> <y2>
agent-browser --session <name> mouse up
```

## Widths and full-page captures

```bash
for width in <widths walked>; do
  agent-browser --session <name> set viewport "$width" 900
  agent-browser --session <name> eval "document.documentElement.scrollWidth <= innerWidth"
  height=$(agent-browser --session <name> eval \
    "Math.max(document.documentElement.scrollHeight, document.querySelector('<scroll-container>')?.scrollHeight ?? 0)")
  agent-browser --session <name> set viewport "$width" "$height"
  agent-browser --session <name> screenshot --full <path>-"$width".png
  agent-browser --session <name> set viewport "$width" 900
done
```
