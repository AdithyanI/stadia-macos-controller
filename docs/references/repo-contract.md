# Mapping and guide release contracts

## Input boundary

`config/mappings.json` is the source of truth. Use explicit `appProfiles`;
`alwaysOn` is a cross-app list, not a fallback profile. Unmapped frontmost apps
receive only `alwaysOn` actions. Keep latency-sensitive Codex controls on direct
keystrokes; `scripts/check-mappings.py` enforces this boundary.

`src/main.swift` owns execution and hot reload. Machine installation, signing,
Accessibility, and physical controller proof are in [deployment](deployment.md).

## Pages guide release

Build command: `python3 scripts/build-controller-guide.py`; output: `dist`;
repository root: `/`; production branch: `main`. The build uses Python's standard
library and reads `CF_PAGES_COMMIT_SHA` (falling back to Git HEAD) for release
identity. Do not build or install the Swift bridge in Pages.

Git-connected Pages builds must include `guide/*`, `config/mappings.json`, and
`scripts/build-controller-guide.py` in their watch paths. Using all repository
paths is also safe. No GitHub Actions deployment is required. Development
machines run `scripts/check-controller-guide-full.sh` before publication;
Pages packages the accepted source.

`/api/mappings` and `/api/health` are 200 aliases to `/api/mappings.json` and
`/api/health.json`. A top-level `404.html` disables implicit SPA fallback.
The output includes no bridge source, configuration other than mappings, or
credentials. All Pages hostnames require Access coverage before upload. See
[Cloudflare redirects](https://developers.cloudflare.com/pages/configuration/redirects/)
and [serving behavior](https://developers.cloudflare.com/pages/configuration/serving-pages/).

Activation is pending verification in the shared migration tracker. Preserve the
existing custom-hostname Access application during DNS cutover and protect the
Pages hostnames separately. Verify exact JSON mapping parity, source SHA,
headers, 404s and authenticated rendering before stopping the old service.

## Retained migration recovery client

`scripts/deploy-controller-guide.sh` is temporarily retained for status,
rollback and uninstall of the old Mac mini guide. It defaults to dry-run and
supports `--apply`, `--status`, `--logs`, `--rollback`, `--uninstall`, `--plain`
and `--no-input`. The old server listens on `127.0.0.1:8798` and holds read-only
releases under `~/.local/share/stadia-controller-guide/production/releases/`.
Uninstall retains releases; remove their exact owned directory and logs after
the one-week rollback window. Remove the retired service's deploy triggers,
tunnel route and health probes at cutover so they cannot restart it. Never
uninstall the separate controller input bridge.
