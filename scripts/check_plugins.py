#!/usr/bin/env python3
"""Checks every plugin in this repo on every change.

Without a generator, each agent tool's files are written by hand, so this
script is what keeps them from drifting apart:
  - every manifest parses and agrees on name, version and description
  - .mcp.json (Claude Code, Codex) and mcp.json (Cursor) are identical
  - every marketplace file lists every plugin folder, and nothing else
  - every skill has name/description frontmatter matching its folder
Usage: python scripts/check_plugins.py [--plugin <folder>]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def load(path, errors):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as e:
        errors.append(f"{path.relative_to(ROOT)}: {e}")
    return None


def frontmatter(path):
    text = path.read_text()
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        return {}
    block = text[4:text.index("\n---", 4)]
    return dict(line.split(":", 1) for line in block.splitlines() if ":" in line)


def check_plugin(folder, errors):
    base = ROOT / "plugins" / folder
    manifests = {m: load(base / m, errors) for m in MANIFESTS}
    manifests = {m: d for m, d in manifests.items() if d is not None}
    for field in ("name", "version", "description"):
        values = {m: d.get(field) for m, d in manifests.items()}
        if len(set(map(str, values.values()))) > 1:
            errors.append(f"plugins/{folder}: '{field}' differs across manifests: {values}")
    claude = manifests.get(".claude-plugin/plugin.json", {})
    if claude and not SEMVER_RE.match(str(claude.get("version", ""))):
        errors.append(f"plugins/{folder}: version '{claude.get('version')}' is not semver")

    mcp, cursor_mcp = load(base / ".mcp.json", errors), load(base / "mcp.json", errors)
    if mcp is not None and cursor_mcp is not None and mcp != cursor_mcp:
        errors.append(f"plugins/{folder}: .mcp.json and mcp.json differ")
    if mcp is not None and not mcp.get("mcpServers"):
        errors.append(f"plugins/{folder}: .mcp.json has no mcpServers")

    skills = sorted(base.glob("skills/*/SKILL.md"))
    if not skills:
        errors.append(f"plugins/{folder}: no skills/*/SKILL.md")
    for skill in skills:
        fm = {k.strip(): v.strip() for k, v in frontmatter(skill).items()}
        if fm.get("name") != skill.parent.name:
            errors.append(f"{skill.relative_to(ROOT)}: frontmatter name must equal folder name")
        if not fm.get("description"):
            errors.append(f"{skill.relative_to(ROOT)}: description is required")
    hooks = base / "hooks/hooks.json"
    if hooks.exists():
        load(hooks, errors)
    return claude.get("name")


def check_marketplaces(names, errors):
    claude = load(ROOT / ".claude-plugin/marketplace.json", errors) or {}
    codex = load(ROOT / ".agents/plugins/marketplace.json", errors) or {}
    cursor = load(ROOT / ".cursor-plugin/marketplace.json", errors) or {}
    listed = {
        ".claude-plugin/marketplace.json": {e["name"]: e["source"].removeprefix("./plugins/") for e in claude.get("plugins", [])},
        ".agents/plugins/marketplace.json": {e["name"]: e["source"]["path"].removeprefix("./plugins/") for e in codex.get("plugins", [])},
        ".cursor-plugin/marketplace.json": {e["name"]: e["source"] for e in cursor.get("plugins", [])},
    }
    for path, entries in listed.items():
        if entries != names:
            errors.append(f"{path}: lists {entries}, expected {names}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plugin", help="check one plugin folder only")
    args = ap.parse_args()
    errors = []
    folders = sorted(p.name for p in (ROOT / "plugins").iterdir() if p.is_dir())
    names = {}
    for folder in folders:
        name = check_plugin(folder, errors)
        if name:
            names[name] = folder
    if not args.plugin:
        check_marketplaces(names, errors)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if not errors:
        print(f"ok: {', '.join(folders)} and marketplace files")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
