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
repository root: `/`; production branch: `main`; Pages project:
`stadia-macos-controller-github`. The build uses Python's standard
library and reads `CF_PAGES_COMMIT_SHA` (falling back to Git HEAD) for release
identity. Set `SKIP_DEPENDENCY_INSTALL=true` in the Pages build environment and
omit `NODE_VERSION` / `PNPM_VERSION`: this standard-library Python build has no
Node package manifest. A forced pnpm install fails before the build starts.
Do not build or install the Swift bridge in Pages.

Git-connected Pages builds must include `guide/*`, `config/mappings.json`, and
`scripts/*` in their watch paths. Using all repository
paths is also safe. No GitHub Actions deployment is required. Development
machines run `scripts/check-controller-guide-full.sh` before publication;
Pages packages the accepted source.

`/api/mappings` and `/api/health` are 200 aliases to `/api/mappings.json` and
`/api/health.json`. A top-level `404.html` disables implicit SPA fallback.
The output includes no bridge source, configuration other than mappings, or
credentials. All Pages hostnames require Access coverage before upload. See
[Cloudflare redirects](https://developers.cloudflare.com/pages/configuration/redirects/)
and [serving behavior](https://developers.cloudflare.com/pages/configuration/serving-pages/).

Cloudflare Access protects the custom hostname and Pages hostnames separately.
Hosted verification covers exact JSON mapping parity, source SHA, headers,
unknown-route 404s and authenticated rendering.

## Retired hosting cleanup

The old Mac mini Python server and guide deployment client are retired. Its
LaunchAgent label was `com.dobby.stadia-controller-guide`; the input bridge is
an independent service and remains installed. The shared migration tracker in
`scripts/docs/projects/static-sites-to-cloudflare-pages/tasks.md` records live
cutover evidence and the one-week rollback deadline. Retain exact owned release
files at `~/.local/share/stadia-controller-guide/production/` and logs at
`~/.local/state/stadia-controller-guide/` until that deadline, then remove them.
Old source remains available through Git history for emergency recovery.
