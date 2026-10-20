# Controller Guide

The guide is a read-only web surface for the bridge configuration. It never
receives controller events and cannot execute or edit actions. The Swift bridge
continues to run on the Mac and hot-reload `config/mappings.json` independently.

## Hosting boundary

The target host is Git-connected Cloudflare Pages at
`https://controller.adithyan.io/`. `scripts/build-controller-guide.py` packages
only the four guide assets, a byte-identical copy of `config/mappings.json`, a
release identity, headers, route aliases, and a 404 page into `dist/`. Pages
publishes this atomic snapshot without a Python server or a home-machine tunnel.
The canonical mappings file remains the only source of action configuration.

`/api/mappings` and `/api/health` are compatibility aliases to static JSON files.
The health response identifies the published commit; it is not bridge health.
Refresh fetches the deployed snapshot. A mapping change reaches the published
guide after its commit to main builds successfully.

Cloudflare Access must protect the custom hostname and all Pages production,
branch, and deployment hostnames before any mappings are uploaded. Exact local
automation mappings remain private-by-authentication. The build also carries the
existing restrictive content security policy and no-store cache policy.

## Migration and local development

The Pages build is prepared; custom-domain activation and old-service retirement
are tracked by `scripts/docs/projects/static-sites-to-cloudflare-pages/tasks.md`.
Until cutover is verified, the existing loopback server and deployment client
remain available for rollback. Their retained releases expire after the
project's rollback window, not merely when the LaunchAgent is uninstalled.

`scripts/run-controller-guide.sh` serves a local development preview on
`127.0.0.1:8173`, rereading checkout mappings on Refresh. It exposes only known
guide routes, never the entire checkout. Unknown routes return 404 in both
hosting models. `guide/app.js` uses the bridge's mapping precedence: enabled
application-profile button mappings override `alwaysOn`; supported analog modes
prefer `alwaysOn` when configured.

## Verification

The guide gate checks mapping semantics, static output isolation, exact mapping
parity, route aliases, security headers, JavaScript syntax, and the retained
local server/deployment contracts. Hosted verification must additionally prove
Access coverage, JSON content types, unknown-route 404 behavior and commit
identity. Bridge behavior requires separate physical-controller verification.
