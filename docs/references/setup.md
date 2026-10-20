# Local run and preview

The bridge needs macOS command-line tools and a connected Stadia controller.
Local execution defaults to dry run:

```bash
./scripts/run-bridge.sh
# Equivalent explicit source invocation:
swift run stadia-controller-bridge --config config/mappings.json
```

Add `--no-dry-run` for live input actions. Use `--prompt-accessibility` when
requesting the required Accessibility permission. For the installed service,
use [deployment and recovery](deployment.md), including its stable app identity.

## Controller guide

```bash
python3 scripts/build-controller-guide.py
python3 -m http.server 8173 --bind 127.0.0.1 --directory dist
```

Open `http://localhost:8173/`; stop it with Control-C. Rebuild after changing
mappings or guide assets, then refresh the browser. Preview serves only the
isolated `dist/` artifact. The page reads `/api/mappings.json`; the old
`/api/mappings` alias is handled by Pages in production.

Run `./scripts/check-controller-guide-full.sh` before publication. Production
uses Git-connected Pages; see [the release contract](repo-contract.md).

## Mappings

The running bridge watches `config/mappings.json`. Code changes need a restart;
new actions or schema require reinstalling the staged launchd binary.
`appProfiles` matches the frontmost bundle ID; only `alwaysOn` controls work
outside a matching profile.

Keep dictation and submit separate. Dictation completion is asynchronous, so
automatic Enter on trigger release can submit partial or previous text.
For Ghostty-specific routing and API constraints, use
`docs/architecture/ghostty-integration.md` and
`docs/references/ghostty-mapping-rationale.md`.
