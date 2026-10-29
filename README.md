# trilio-plugins

Every Trilio SKU's agent plugins in one repo, split by folder. This repo is
also the marketplace customers add. This is **Option B (single repo)** in the
*Agent Plugins: Repository Structure Proposal*.

```
trilio-plugins/
├── .claude-plugin/marketplace.json   ← lists every SKU plugin (Claude Code)
├── .agents/plugins/marketplace.json  ← same list for Codex
├── .cursor-plugin/marketplace.json   ← same list for Cursor
├── .github/CODEOWNERS                ← plugins/tsr → TSR team, plugins/t4k → T4K team
├── plugins/
│   ├── tsr/   (.claude-plugin/, .codex-plugin/, .cursor-plugin/, .mcp.json, mcp.json, skills/, agents/, hooks/)
│   └── t4k/   (.claude-plugin/, .codex-plugin/, .cursor-plugin/, .mcp.json, mcp.json, skills/, hooks/)
├── evals/{tsr,t4k}/                  ← eval cases per SKU
├── scripts/check_plugins.py          ← the one CI check for every plugin
└── tests/
```

## Install

**Claude Code**

```sh
claude plugin marketplace add somesh22123/trilio-plugins
claude plugin install site-recovery-kubernetes@trilio-plugins
claude plugin install trilio-t4k-guide@trilio-plugins
```

**Codex**

```sh
codex plugin marketplace add somesh22123/trilio-plugins
```

## Day to day

1. Each SKU team edits only its own folder; CODEOWNERS routes reviews to that team.
2. One CI pipeline (`scripts/check_plugins.py` + tests) checks every plugin on every change.
3. Each plugin keeps its own version and tag prefix, so TSR and T4K release separately:
   bump `version` in all three of the plugin's manifests, then tag `site-recovery-kubernetes/v0.2.0`.
4. Customers add this repo once and install any plugin from it.

## No generator (yet)

Each agent tool's files are written by hand. `check_plugins.py` catches drift
between them: name, version and description must agree across
`.claude-plugin/`, `.codex-plugin/` and `.cursor-plugin/`, `.mcp.json` must
equal `mcp.json`, and every marketplace file must list exactly the plugin
folders. A generator can be added later inside this repo.

Keep each plugin folder self-contained, so a SKU can be split into its own
repo later without untangling shared files.

## Adding a SKU

1. Copy `plugins/t4k/` to `plugins/<sku>/` and rename inside it.
2. Add the plugin to all three marketplace files.
3. Add the folder to `.github/CODEOWNERS`.
4. Run `python scripts/check_plugins.py`.
