# Controller Guide

The guide is a read-only web surface for the bridge configuration. It never
receives controller events and cannot execute or edit actions. The Swift bridge
continues to run on the Mac and hot-reload `config/mappings.json` independently.

## Hosting boundary

The host is Git-connected Cloudflare Pages (project `stadia-macos-controller-github`) at
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

## Local development and retired hosting

Build `dist/` then preview it with Python's standard static server; commands are
in [setup](../references/setup.md). Rebuild after mapping edits. The page reads
`/api/mappings.json` directly; Pages retains extensionless aliases for existing
consumers. Unknown routes return 404 in both environments.

The former Mac mini guide server, release client and dedicated LaunchAgent are
retired. The shared migration tracker records operational cutover and removal
of retained releases/logs after the one-week rollback window. The input bridge
remains on the Mac and is unaffected by guide hosting.

`guide/app.js` uses the bridge's mapping precedence: enabled application-profile
button mappings override `alwaysOn`; supported analog modes prefer `alwaysOn`
when configured.

## Verification

The guide gate checks mapping semantics, static output isolation, exact mapping
parity, route aliases, security headers, JavaScript syntax and static HTTP routes. Hosted verification must additionally prove
Access coverage, JSON content types, unknown-route 404 behavior and commit
identity. Bridge behavior requires separate physical-controller verification.
